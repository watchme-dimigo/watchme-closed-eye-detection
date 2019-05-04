# WatchMe Backend

## main
현재 눈 감김 여부를 연속적으로 출력

```json
{"closed": 0}
```

- `-1`: 얼굴을 찾지 못함
- `0`: 눈을 뜨고 있음(false)
- `1`: 눈을 감고 있음(true)

## customize
- 각 사용자에 맞게 적절한 값의 `ear_thresh`를 구해 커스터마이제이션을 도움

### 구현
1. 일정 
