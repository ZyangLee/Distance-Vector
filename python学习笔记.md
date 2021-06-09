# python学习笔记

### 变量类型

* 整型：python3对int和long不加区分
* 浮点型：小数
* 字符串：单括号或者双括号括起来的文本
* 布尔型：True，False
* 复数型：3+5j，将数学中i换成j
* 使用type()可以对变量类型进行检查

### 变量命名

* PEP 8要求：
  * 小写字母拼写，多个单词用下划线连接
  * 受保护的实例属性用单个下划线开头
  * 私有的实例属性用两个下划线开头

### 函数

使用`def`关键字定义函数，python中对函数参数的处理时，参数可以有默认值，也可以使用可变参数，所以不需要进行函数的重载，**传递参数时可以不按照设定的顺序进行传递**。

```python
def add(a=0, b=0, c=0):
    return a + b + c

print(add(c = 1, b = 2, a = 3))
```

如果不确定参数个数，可以使用可变参数（*）

```python
# 在参数名前面的*表示args是一个可变参数，在调用该函数时可以传入0或多个参数
def add(*args):
    total = 0
    for var in args:
        total += val
    return total
```

### 模块管理函数

由于Python没有函数重载的概念，后面的定义会覆盖之前的定义，意味着两个同名函数只有最后那个会存在。**Python中每一个文件就代表了一个模块（module）**，在不同的模块中可以有同名的函数，通过import导入指定的模块可以区分同名函数。

`module1.py`

```python
def foo():
	print('hello')
    
```

`module2.py`

```python
def foo():
    print('bye')
```

`test.py`

```python
import module1 as m1
import module2 as m2
m1.foo()
m2.foo()
```

如果导入的模块除了定义函数之外还有其他的可执行代码，导入时就会执行这些代码，如果不希望这些代码被导入，则需要将这些代码写进if条件下，代码如下：

`module3.py`

```python
def foo():
    pass
def bar():
    pass

# __name__ 是python中一个隐含的变量，代表了模块的名字
# 只有被python解释器直接执行的模块的名字才是__main__
if __name__ == '__main__':
    foo()
    bar()
```

`test.py`

```python
import module3

# 导入module3时，不会执行模块中if条件成立时的代码，因为模块的名字是module3而不是__main__
```

#### 实现计算求最大公约数和最小公倍数的函数

```python
def gcd(x, y):
    """求最大公约数"""
    (x, y) = (y, x) if x > y else (x, y)  # 将小的数放在前面
    for factor in range(x, 0, -1):
        if x % factor == 0 and y % factor == 0:
            return factor
        
        
 def lcm(x, y):
    """求最小公倍数"""
    return x * y // gcd(x, y)
```

### 变量的作用域

```python
def foo():
    b = 'hello'
    
    def bar():
        c = True
        print(a)
        print(b)
        print(c)
        
    bar()
    
    
if __name__ == '__main__':
    a = 100
    # print(b)  # b is not defined
    foo()
```

* 对上面的a、b、c 变量进行分析
  * `a`是一个全局变量（global variable），因为其没有定义在任何一个函数中，属于全局作用域
  * `b`，c是一个函数中的局部变量（local variable），在函数的外部不能直接访问
  * 对于bar函数中的`b`，属于**嵌套作用域**
* python查找一个变量时会按照“局部作用域、嵌套作用域、全局作用域、标识符”顺序进行搜索

#### 在函数内修改全局变量值

```python
def foo():
    global a  # 如果不写global，会重新定义名字为a的局部变量
    a = 200

    
if __name__ == '__main__':
    
    a = 100
    foo()
    print(a)  # 100
```

如果希望在函数内修改嵌套作用域中的变量，可以使用`nonlocal`关键字来指示变量来自于嵌套作用域。

* 应该减少对全局变量的使用（降低代码耦合度的一个重要举措），尽量让变量的作用域为函数的内部，如果需要将要给局部变量生命周期延长，使其在定义它的函数调用结束后依然使用它的值，就需要使用闭包。

* 推荐python代码写法：

  ```python
  def main():
  	pass
  if __name__ == 'main':
      main()
  ```

  



### 字符串

* 表示方法：‘abc’， “abc ”，“”“ ”“” 以三个双引号或单引号开头的字符串可以拆行

* \  表示转义符，字符串中表示`'`要写成`\'`，如果不希望\  表示转义，可以通过在字符串的最前面加上字母r

  ```python
  s1 = '\'hello, world!\''  #  结果： \'hello, world!\'
  s2 = '\n\\hello, world!\\\n'  #  结果： \n\\hello, world!\\\n
  print(s1, s2, end='')
  ```

* 可以使用”+“实现字符串拼接，用 * 实现字符串的重复，用`in`  和 `not in` 来判断一个字符串是否包含另一个字符串（成员运算）

  ```python
  print('ll' in s1) # True
  print('good' in s1) # False
  str2 = 'abc123456'
  # 从字符串中取出指定位置的字符(下标运算)
  print(str2[2]) # c
  # 字符串切片(从指定的开始索引到指定的结束索引)[起点：终点：步长]
  print(str2[2:5]) # c12
  print(str2[::-1]) # 654321cba
  print(str2[-3:-1]) # 45
  ```

  #### 常用的字符串处理函数

  ```python
  str1 = "123abc"
  # 获得子串长度
  len(str1)  # 6
  
  # 查找子串所在位置
  str1.find('123')  # 0
  str1.find('456')  # -1
  
  # 检查是否以指定字符串开头或以指定字符串结尾
  str1.startswith('123')  # True
  str1.endswith('abc')  # True
  
  # 检查字符串是否由数字、字母、或者数字和字母构成
  str1.isdigit()
  str1.isalpha()
  str1.isalnum()
  
  # 获得字符串修剪左右两侧空格之后的拷贝
  str1.strip()
  
  # 字符串的方式格式化输出，字符串前加上字母f
  a, b = 5, 10
  print('{0} * {1} = {2}'.format(a, b, a * b))
  
  # 拆分字符串
  str.split(str="", num=string.count(str))
  '''
  str -- 分隔符，默认为所有的空字符包括空格、换行(\n)、制表符(\t)等
  num -- 分割次数。默认为 -1, 即分隔所有
  '''
  str = "this is string example....wow!!!"
  print (str.split( ))       # 以空格为分隔符
  ['this', 'is', 'string', 'example....wow!!!']
  
  # 如果需要用更复杂的、或者多种字符进行分割，需使用正则表达式
  import re
  re.split(r'<正则表达式>', str)
  re.split(r'[+-]', str)  # 利用+或-分割字符串
  
  
  # python3.6的更简洁书写方式
  print(f'{a} * {b} = {a * b}')
  
  ```


#### 字符串前加u，r，b的含义

* 字符串前加'u'：

后面字符串以Unicode格式进行编码，一般在中文字符串的前面，防止因为源码存储格式的问题，导致再次使用

* 字符串前加’r‘：

去掉反斜杠的转移机制

* 字符串前加’b'：

表示后面的字符串是bytes类型。

* bytes与str互相转换：

`str.encode('utf-8')`

`bytes.decode('utf-8')`



### 列表

* 如何定义列表和**遍历方式**

  ```python
  list1 = [1, 3, 5, 7, 100]
  # 计算列表长度
  print(len(list1))  # 5
  # 通过循环用下标遍历列表元素
  for index in range(len(list1)):
      print(list[index])
  # 直接遍历列表元素
  for elem in list1:
      print(elem)
  # 使用enumerate函数处理列表之后可以同时获得元素索引和值
  for index, elem in enumerate(list1):
      print(index, elem)
  ```

* 添加元素和移除元素

  ```python
  # 添加元素
  list1.append(200)  # 添加在列表末尾
  list1.insert(1, 400)  # (下标位置，元素)
  list1 += [1000, 2000]
  
  # 删除元素，删除指定元素前需要先判断是否在列表中
  if 3 in list1:
      list1.remove(3)
  
  # 从指定位置删除元素
  list1.pop(0)  # 删除下标为0的元素
  
  # 清空列表元素
  list1.clear()
  ```

* 切片

  ```python
  list2 = list[1:4]  # list[1], list[2], list[3]
  # 可以通过完整的切片复制列表，直接list2 = list是浅拷贝
  list2 = list[:]
  # 可以通过反向切片操作实现倒转之后列表的拷贝
  list3 = list[::-1]
  ```

* 排序

  ```python
  # sorted函数返回列表排序后的拷贝不会修改传入的列表
  list2 = sorted(list)
  # 修改排序关键字
  list3 = sorted(list, key=len, reverse=False)
  # 给列表发出排序信息后直接在列表对象上进行排序
  list1.sort()  # 可以修改key和reverse
  
  ```

* 生成式创建列表和使用生成器

  ```python
  f = [x for x in range(1, 10)]
  f = [x + y for x in 'ABCDE' for y in '1234567']  # 35个元素的列表，for循环的嵌套
  
  # f是一个生成器对象，通过生成器可以获取到数据
  # 每次需要数据的时候，生成器通过内部运算得到数据（需要花费额外的时间）
  f = (x ** 2 for x in range(1, 1000))
  
  
  # 定义一个返回生成器的斐波那契数列
  def fib(n):
      a, b = 0, 1
      for _ in range(n):
          a, b = b, a + b
          yield a
  
  
  def main():
      for val in fib(20):
          print(val)
  
  
  if __name__ == '__main__':
      main()
  
  ```

### 元组

相比于list，元组具有元素不能修改的特性

```python
# 定义元组
t = ('lza', 21, True, 'jinzhou')
# 将元组转换为列表
person = list(t)
# 将列表转换为元组
person_tuple = tuple(person)

```

*  为什么有了列表之后还需要元组这种类型？
  * 元组中的元素无法修改，一个不变的对象更容易维护。如果不需要对元素进行添加，删除，修改的时候，可以考虑使用元组。一个方法要返回多个值时，也使用元组。
  * 元组在创建时间和占用空间上都优于列表。

### 集合

python 中的集合和数学上集合一致，不允许有重复元素，而且可以进行交集、并集、差集运算

```python
set1 = {1, 2, 3, 3, 3}
# 构造器语法
set2 = set(range(1, 10))
set3 = set((1, 2, 3, 3, 2, 1))

# 创建集合的推导式语法
set4 = {num for num in range(1, 100) if num % 3 == 0}

# 添加、删除元素
set1.add(4)
set1.update([5, 6])  # 追加两个元素
if 4 in set1:
    set1.remove(4)
set1.pop()

# 集合的交集、并集、差集、对称差运算
set1 & set2
set1 | set2
set1 - set2
set1 ^ set2
```

### 字典

字典与列表、集合不同的是，字典中的每个元素都是由一个键和一个值组成的键值对，键和值通过冒号分开。

```python
# 创建字典的字面量语法
scores = {'q':1, 'w':2}
# 创建字典的构造器语法
items1 = dict(one = 1, two = 2)
# 创建字典的推导式语法
items2 = {num: num ** 2 for num in range(1, 10)}
# 通过键可以获得字典中对应的值
print(scores['q'])
# 对字典中所有的键对进行遍历
for key in scores:
    print(f'{key}: {scores[key]}')
# 删除字典中元素，pop内为指定的键值
scores.pop('q')
scores.pop('e', 'error')  # 'e'在字典中不存在，所以返回指定内容('error')
# 清空字典
scores.clear()
```

### 练习

#### 1. 在屏幕上显示跑马灯文字

```python
import os
import time

content = 'abcdefghijklmnopqrstuvwxyz'
while True:
    # 清理屏幕上输出
    os.system('cls')  # os.system('cls')
    print(content)
    # 休眠200ms
    time.sleep(0.2)
    content = content[1:] + content[0]  # 字符串切片
```



## 面向对象

### 定义类

在python中可以用class定义类，用函数定义类中的方法

```python
class Student(object):
    
    # __init__是一个特殊方法，用于创建对象时的初始化操作
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def study(self, course_name):
        print('%s正在学习%s.' % (self.name, course_name))
```

### 创建和使用对象

```python
def (main):
    # 创建学生 对象 并指定姓名和年龄
    stu1 = Student('lza', 21)
    # 给创建的学生对象发送study 消息
    stu1.study('python')


if __name__ == 'main':
    main()
```

### 访问权限

在Python中，属性和方法的访问权限只有两种：公开和私有，如果希望属性是私有的，在**属性命名时可以用两个下划线为开头**。

```python
class Test:
    
    def __init__(self, foo):
        self.__foo = foo  # 创建私有属性
    
    def __bar(self):
        print(self.__foo)  # 可以访问私有变量
        print('__bar')
        
        
    def main():
        test = Test('hello')
        test.__bar()  # 无法在外部访问私有方法
```

实际开发中，不建议将属性设置为私有的，这样会导致子类无法访问，应遵循一种让**属性名以单下划线开头的方式表示属性是受保护**的，本类之外的代码访问这样的属性时应该慎重（**这种做法不是语法上的规则**）

* 面向对象的三大支柱
  * 封装：隐藏一切可以隐藏的实现细节，向外界提供简单的编程接口
  * 继承
  * 多态



### @property装饰器

单下划线标识的受保护的属性，不建议外界直接访问，规定访问受保护属性需要通过getter（访问器）和setter（修改器）方法进行相应的操作，用property包装器包装getter和setter方法，可以达到对属性访问的目的。

```python
 class Person(object):
        
        def __init__(self, name, age):
            self._name = name
            self._age = age
        
        # 访问器
        @property
        def name(self):
            return self._name
        
        @property
        def age(self):
            return self._age
        
        # 修改器 - setter方法
        @age.setter
        def age(self, age):
            self._age = age
```

@property 会将方法转换为只读属性，这样可以防止属性被修改，注意调用修饰后的方法时，用调用属性的方式调用该方法。

```python
def main():
    person = Person('wang', 21)
    print(person.age)  # 通过getter访问保护属性
    person.age = 22  # 使用setter
```



### \_\_slots\_\_魔法

Python是动态语言，动态语言允许**在程序运行的过程中给对象绑定新的属性或者方法**。如果我们需要限定自定义类型的对象只能绑定某些属性，可以通过在类中定义 \_\_slots\_\_变量来进行**限定**。注意：**\_\_slots\_\_的限定只对当前类的对象生效，对子类不起任何作用。**

```python
class Person(object):
    
    # 限定Person对象只能绑定_name, _age和gender属性
    __slots__ = ('name', 'age', 'gender')
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
 
def main():
    person = Person('v', 25)
    person.gender = '男'  # 给对象绑定了新属性gender
    
    # AttributeError: 'Person' object has no attribute 'hometown'
    person.hometown = 'kkk'    
```



### 静态方法和类方法

我们在类中定义的方法都是对象方法，这些方法都是发送给对象的消息。但是如果我们需要写一个**尚未创建对象时需要使用的方法**，这类方法就是静态方法。staticmethod方法不需要表示自身类的cls函数

示例：检查三角形三边长度是否满足三角形条件

```python
for math import sqrt

class Trianle(object):
    
    def __init__(self, a, b, c):
        self._a = a
        self._b = b
        self._c = c
    
    @staticmethod
    def is_valid(a, b, c):
        return a + b > c and b + c > a and a + c > b
```

与静态方法比较类似，Python中还可以在类中定义方法，类方法的**第一个参数名约定为cls**，它代表的是自身类，通过这个参数我们可以获取和类相关的信息并且**可以创建出类的对象**

示例：根据当前时间创建数字时钟

```python
from time import time, localtime, sleep

class Clock(object):
    def __init__(self, hour=0, minute=0, second=0):
        self._hour = hour
        self._minute = minute
        self._second = second
    
    @classmethod
    def now(cls):  
        ctime = localtime(time())
        return cls(ctime.tm_hour, ctime.tm_min, ctime.tm_sec)
    

def main():
    # 通过类的方法获取系统时间并创建对象
    clock = Clock.now()
```



### 继承和多态

提供继承信息的称为父类（超类或者基类），得到继承信息的为子类（派生类或衍生类）。

实际开发中，通常会**用子类对象去替换掉一个父类对象**，这是面向对象编程中一个常见的行为（里氏替换原则）

```python
class Person(object):
    
    def __init__(self, name, age):
        self._name = name
        self._age = age
        
   	@property
    def name(self):
        return self._name
    
    @property
    def age(self):
        return self._age
    
    def play(self):
        print('playing')
    
    
class Student(Person):
    
    def __init__(self, name, age, grade):
        super().__init__(name, age)
        self._grade = grade
```

子类继承父类的方法后，可以对父类已有的方法给出新的实现版本，即**重写（override）**，调用这个经过子类重写的方法时，不同子类对象**对于同种方法表现出不同的行为**，即**多态（poly-morphism）**。

抽象类是不能够创建对象的类，这种类的存在就是为了让其他的类去继承它。python实现抽象类需要通过abc模块的`ABCMeta`元类和`abstractmethod`包装器来达到抽象类的效果，当一个类存在抽象方法，那这个类就不能够实例化（创建对象）。

```python
from abc import ABCMeta, abstractmethod

class Pet(object, metaclass=ABCMeta):  # 此处使用metaclass=ABCMeta
    
    def __init__(self, nickname):
        self._nickname = nickname
        
    @abstractmethod  # 表示抽象方法
    def make_voice(self):
        """发出声音"""
        pass
    
    
class Dog(Pet):
    
    def make_voice(self):
        print(f'{self._nickname}: wangwangwang')
        
class Cat(Pet):
    
    def make_voice(self):
        print(f'{self._nickname}: miaomiaomiao')
        
        
def main():
    pets = [Dog('旺财'), Cat('凯蒂')]
    for pet in pets:
        pet.make_voice()
```



### 文件和异常

python中文件读写操作使用内置的`open`函数，可以指定文件名、操作模式、编码信息来获得操作文件的对象。操作模式如下表所示：
| 操作模式 | 具体含义                                             |
| -------- | ---------------------------------------------------- |
| `'r'`    | 读取 （默认）                                        |
| `'w'`    | 写入（会先截断之前的内容），可创建新文件。`w+`可读写 |
| `'x'`    | 写入，如果文件已经存在会产生异常                     |
| `'a'`    | 追加，将内容写入到已有文件的末尾。可创建新文件       |
| `'b'`    | 二进制模式，rb：读取二进制文件                       |
| `'t'`    | 文本模式（默认）                                     |
| `'+'`    | 更新（既可以读又可以写）`r+`：可读可写               |



### 读写文本文件

读取文本文件时，使用`open`函数时指定好带路径的中文名（可以使用**相对路径或者绝对路径**），并将文件模式设置为`'r'`（默认值就是r），然后通过`encoding`参数指定编码（默认是操作系统默认的编码）。如果文件编码方式与指定编码方式不一致，可能会因无法解码字符导致读取失败。

```python
def main():
    f = open('test.txt', 'r', encoding='utf-8')
    print(f.read())  # read（）方法实现全文读取
    f.close()
    
if __name__ == '__main__':
    main()
```

除了`read`方法，还有`for-in`循环逐行读取和`readlines`方法可以将文件按行读取到一个列表容器中。

```python
def main():
    
    # 通过for-in循环逐行读取
    with open('test.txt', mode='r') as f:
        for line in f:
            print(line, end=' ')
            time.sleep(1)
            
    
    # 读取文件按行读取到列表中，每一行是列表里的一个元素（包括\n）
    with open('test.txt') as f:
        lines = f.readlines()
    print(lines)
```



文本信息写入文本文件，需要在open函数指定好文件名并将文件格式设置为'w' 即可。如果是追加是写入，需要将模式设置为'a'

```python
with open('test.txt', 'w') as f:
    f.write(str(12345) + '\n')
```



### 异常情况处理

上面的方法读写文本文件时，如果文件打开出现问题，将会导致程序崩溃。因此，可以使用`try`代码块，配合`except`来捕获可能出现的异常状况。不管是否出现异常，程序都会执行`finally`块的代码。（即使执行`exit`退出环境，`finally`块也会被执行，因为exit函数实质上是引发了`SystemExit`异常），finally块被称为总是执行代码块，**`finally`适合用来释放外部资源**。

```python
def main():
    f = None
    try:
        f = open('致橡树.txt', 'r', encoding='utf-8')
        print(f.read())
    except FileNotFoundError:
        print('无法打开指定的文件!')
    except LookupError:
        print('指定了未知的编码!')
    except UnicodeDecodeError:
        print('读取文件时解码错误!')
    finally:
        if f:
            f.close()
```

**上下文语法**也可以实现自动释放资源，通过`with`关键字指定文件的上下文环境并在**离开上下文环境时自动释放文件资源**。

```python
def main():
    try:
        with open('致橡树.txt', 'r', encoding='utf-8') as f:
            print(f.read())
    except FileNotFoundError:
        print('无法打开指定的文件!')
    except LookupError:
        print('指定了未知的编码!')
    except UnicodeDecodeError:
        print('读取文件时解码错误!')
```



### 读写二进制文件

通过读写二进制文件实现复制图片文件的功能

```python
def main():
    try:
        with open('lenna.jpg', 'rb') as fs1:
            data = fs1.read()
            print(type(data))  # <class 'bytes'>
        with open('莱纳.jpg', 'wb') as fs1:
            fs2.write(data)
    except FileNotFoundError as e:
        print("指定文件无法打开")
    except IOError as e:
        print('读写文件时出现错误')
    print('程序执行结束')
```



### 读写JSON文件

python希望将列表或者字典中的数据保存在文件中，此时需要JSON格式进行保存。JSON是”JavaScript Object Notation“的缩写，广泛用于**跨平台跨语言数据交换**。由于JSON也属于纯文本，所以任何语言都可以处理纯文本。[JSON的官方网站](http://json.org)

```json
{
    "name": "骆昊",
    "age": 38,
    "qq": 957658,
    "friends": ["王大锤", "白元芳"],
    "cars": [
        {"brand": "BYD", "max_speed": 180},
        {"brand": "Audi", "max_speed": 280},
        {"brand": "Benz", "max_speed": 320}
    ]
}
```

上面可以看出JSON和Python字典一样，实际上json数据类型和python数据类型有对应关系。

| JSON                | Python       |
| ------------------- | ------------ |
| object              | dict         |
| array               | list         |
| string              | str          |
| number (int / real) | int / float  |
| true / false        | True / False |
| null                | None         |

使用json模块**将字典或列表以json格式保存**到文件中

```python
import json


def main():
    mydict = {
        'name': '骆昊',
        'age': 38,
        'qq': 957658,
        'friends': ['王大锤', '白元芳'],
        'cars': [
            {'brand': 'BYD', 'max_speed': 180},
            {'brand': 'Audi', 'max_speed': 280},
            {'brand': 'Benz', 'max_speed': 320}
        ]
    }
    try:
        with open('data.json', 'w', encoding='utf-8') as fs:
            json.dump(mydict, fs)  # 使用json中的dump方法
    except IOError as e:
        print(e)
    print('保存数据完成!')


if __name__ == '__main__':
    main()
```

json模块的四个重要函数：

* dump -将Python对象转到JSON格式文件中
* dumps：将Python对象处理为JSON格式的字符串
* load：将文件中JSON数据反序列化成Python对象
* loads：将JSON字符串内容反序列化成Python对象



### 正则表达式

处理字符串程序时，经常会有查找符合某些复杂规则的字符串的需要。正则表达式就是**记录文本规则的代码**。



### 用Pillow操作图像

Pillow是可以实现图像压缩和图像处理的库，其中读取和处理图像都要用到**Image**类

#### 读取图像和基本的图像处理

```python
from PIL import Image
image = Image.open('./desktop/lenna.jpg')

# 剪裁图像
rect = 80, 20, 310, 360
image.crop(rect).show()

# 生成缩略图 thumbnail
size = 128, 128
image.thumbnail(size)

# 缩放 resize
image_resize = image.resize(int(width / 1.5), int(height / 1.5))

# 旋转和翻转
image.rotate(180).show()  # 将图片旋转180度并展示
image.transpose(Image.FLIP_LEFT_RIGHT).show()

# 操作像素
image.putixel((x, y), (0, 0, 255))  # RGB, 将x，y位置的像素设置为蓝色

```

