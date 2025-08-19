// 利用AST技术,尽可能将运行过程中的所有变量注册到window中,最后统一输出,从而方便用户调试分析

const parser = require('@babel/parser');
const traverse = require('@babel/traverse').default;
const t = require('@babel/types');
const generator = require('@babel/generator').default;
const fs = require('fs');

function randomString(len = 6) {
    return Math.random().toString(36).substring(2, 2 + len);
}

const code = fs.readFileSync('xxx.js', 'utf-8');
const codeLines = code.split('\n');
const ast = parser.parse(code, { sourceType: 'script' });

const windowVars = []; // 用于收集插桩变量名

traverse(ast, {
    VariableDeclaration(path) {
        path.node.declarations.forEach(decl => {
            const line = decl.loc?.start?.line || path.node.loc?.start?.line || 0;
            try {
                if (t.isIdentifier(decl.id)) {
                    const varName = decl.id.name;
                    const winKey = `${varName}_${randomString()}_L${line}`;
                    const setGlobal = t.expressionStatement(
                        t.assignmentExpression(
                            '=',
                            t.memberExpression(t.identifier('window'), t.identifier(winKey)),
                            t.identifier(varName)
                        )
                    );
                    path.insertAfter(setGlobal);
                    windowVars.push(winKey);
                }
            } catch (e) {
                const srcLine = codeLines[line - 1]?.trim() || '[未知源码]';
                console.log(`[插桩异常] 第${line}行源码：${srcLine}\n异常信息：${e.message}`);
            }
        });
    }
});

// 在插桩后的文件末尾输出所有 window 注册变量
if (windowVars.length > 0) {
    const logVars = t.expressionStatement(
        t.callExpression(
            t.memberExpression(t.identifier('console'), t.identifier('log')),
            [
                t.stringLiteral('[window变量输出]'),
                t.objectExpression(
                    windowVars.map(name => t.objectProperty(
                        t.stringLiteral(name),
                        t.memberExpression(t.identifier('window'), t.identifier(name))
                    ))
                )
            ]
        )
    );

    // 在 AST 的末尾插入输出语句
    ast.program.body.push(logVars);
}

const output = generator(ast, {}, code);
fs.writeFileSync('xxx.instrumented.js', output.code);
console.log('Instrumented file generated: pagination16.instrumented.js');