# 함수 생성
def func_1(x, y):
    result = 0

    for i in range(min(x, y), max(x, y)+1, 1):
        result += i
        
    return result

# 함수 호출
print(func_1(1, 10))

def func_2(x,y):
    result = x + y
    return result

print(func_2(10, 4))

# 변수 생성
text = 'Hello World'

print(text)