#!/bin/bash
INPUT=$(cat)

# 編集されたファイルパスを取得
FILE_PATH=$(echo "$INPUT" | python3 -c "
import json, sys
d = json.load(sys.stdin)
files = d.get('tool_input', {}).get('files', [])
# TSファイルのみ対象
ts_files = [f for f in files if f.endswith('.ts')]
print('\n'.join(ts_files))
" 2>/dev/null || echo "")

# TSファイルがなければスキップ
if [ -z "$FILE_PATH" ]; then
  exit 0
fi

# ESLintを実行
ESLINT_OUTPUT=$(npx eslint $FILE_PATH --format=compact 2>&1)
EXIT_CODE=$?

# 出力がなければ（エラーも警告もなし）スキップ
if [ -z "$ESLINT_OUTPUT" ]; then
  exit 0
fi

# 警告メッセージをCopilotに伝える
python3 -c "
import json, sys
output = sys.argv[1]
result = {
    'hookSpecificOutput': {
        'hookEventName': 'PostToolUse',
        'additionalContext': f'ESLint の検査結果:\n{output}\n\n上記の問題を修正してください。'
    }
}
print(json.dumps(result, ensure_ascii=False))
" "$ESLINT_OUTPUT"
