import time


def count_time(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        func(*args, **kwargs)
        print("执行时间为：", time.time() - t1)

    return wrapper


def baiyu():
    print("我是攻城狮白玉")
    time.sleep(2)


@count_time
def blog(name):
    print('进入blog函数')
    name()
    print('我的博客是 https://blog.csdn.net/zhh763984017')


if __name__ == '__main__':
    # baiyu = count_time(baiyu)  # 因为装饰器 count_time(baiyu) 返回的时函数对象 wrapper，这条语句相当于  baiyu = wrapper
    # baiyu()  # 执行baiyu()就相当于执行wrapper()

    # baiyu()  # 用语法糖之后，就可以直接调用该函数了
    blog(baiyu)