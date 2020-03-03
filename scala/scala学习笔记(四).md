### 函数

在scala中,不仅可以定义一个函数然后调用它，还可以写一个未命名的函数字面量，然后把他当成一个值，传递到其它函数或是赋值给其它变量。

```scala
(x:Int) => x+1
```

这是个函数字面量，它的功能为 `+1` 。符号 `=>` 表示这个函数将符号左边的东西（本例为一个整数），转换成符号右边的东西（加 1 ）。

函数字面量为一个对象（就像 `3` 是个对象）。因此，如果你愿意的话，可以把这个函数字面量保持在一个变量中。这个变量也是一个函数，因此你可以使用函数风格来调用它，比如：

```scala
scala> var increase = (x :Int ) => x +1
increase: Int => Int = <function1>
scala> increase(10)
res0: Int = 11
```

函数字面量`(x:Int)=>x+1`在scala内部，表示为带有一个参数的类function1的一个对象。其它情况比如functionN代表带有N个参数的函数,function0代表不含参数的函数类型

注意，函数字面量 `(x:Int) => x + 1` 在 Scala 内部，表示为带有一个参数的类 `function1` 的一个对象。其它情况比如 `functionN` 代表带有 N 个参数的函数， `function0` 代表不含参数的函数类型。

如果函数定义需要多条语句，可以使用 `{}` ，比如：

```
scala> var increase = (x :Int ) => {
     |    println("We")
     |    println("are")
     |    println("here")
     |    x + 1
     |    }
increase: Int => Int = <function1>

scala> increase (10)
We
are
here
res0: Int = 11
```

从上面的内容中，我们了解到了函数字面量的基本概念。它可以作为参数传递给其它函数，比如很多 Scala 的库允许你使用函数作为参数（比如 foreach 方法，它使用一个函数参数，为集合中每个运算调用传入的函数）。例如：

```
scala> val someNumbers = List ( -11, -10, - 5, 0, 5, 10)
someNumbers: List[Int] = List(-11, -10, -5, 0, 5, 10)

scala> someNumbers.foreach((x:Int) => println(x))
-11
-10
-5
0
5
10
```

再比如，Scala 的集合也支持一个 `filter` 方法用来过滤集合中的元素，`filter` 的参数也是一个函数，比如：

```
scala> someNumbers.filter( x => x >0)
res1: List[Int] = List(5, 10)
```

使用 `x => x >0`，过滤掉小于 `0` 的元素。如果你熟悉 `lambda`表达式， `x => x >0` 为函数的 `lambda` 表达式。

Scala 还可以进一步简化：Scala 允许使用“占位符”下划线“`_`”来替代一个或多个参数，只要这个参数值函数定义中只出现一次，Scala 编译器可以推断出参数。比如：

```
scala> val someNumbers = List ( -11, -10, - 5, 0, 5, 10)
someNumbers: List[Int] = List(-11, -10, -5, 0, 5, 10)

scala> someNumbers.filter(_ >0)
res0: List[Int] = List(5, 10)
```

可以看到，简化后的函数定义为 `_ > 0` ，你可以这样来理解：就像我们以前做过的填空题，“ `_` ”为要填的空，Scala 会来完成这个填空题，而你来定义填空题。

有时，如果你使用 `_` 来定义函数，可能没有提供足够的信息给 Scala 编译器。此时， Scala 编译器将会报错。比如，定义一个加法函数如下：

```
scala> val f = _ + _
<console>:7: error: missing parameter type for expanded function ((x$1, x$2) => x$1.$plus(x$2))
       val f = _ + _
               ^
<console>:7: error: missing parameter type for expanded function ((x$1: <error>, x$2) => x$1.$plus(x$2))
       val f = _ + _
```

Scala 编译器无法推断出 `_` 的参数类型，所以报错了。但如果你给出了参数的类型，就依然可以使用 _ 来定义函数。比如：

```
scala> val f = (_ :Int ) + ( _ :Int)
f: (Int, Int) => Int = <function2>

scala> f (5,10)
res1: Int = 15
```

因为 `_` 替代的参数在函数体中只能出现一次，因此多个“ `_` ”代表多个参数。第一个“ `_` ”代表第一个参数，第二个“ `_` ”代表第二个参数，以此类推。

前面的例子中，我们使用了 “`_`” 来代替单个的参数。实际上，你也可以使用 “`_`” 来代替整个参数列表。比如说，你可以使用 `println _` 来代替 `println (_)`。

```
someNumbers.foreach(println _)
```

Scala 编译器自动将上面代码解释成：

```
someNumbers.foreach( x => println (x))
```

因此这里的 “`_`” 代表了 `println` 的整个参数列表，而不仅仅替代单个参数。

当你采用这种方法使用 “`_`” ，你就创建了一个部分应用的函数(partially applied function)。在 Scala 中，当你调用函数，传入所需参数，你就把函数“应用”到参数。比如：一个加法函数。

```
scala> def sum = (_:Int) + (_ :Int) + (_ :Int)
sum: (Int, Int, Int) => Int

scala> sum (1,2,3)
res0: Int = 6
```

一个部分应用的函数指的是你在调用函数时，不指定函数所需的所有参数。这样，你就创建了一个新的函数，这个新的函数就称为原始函数的`部分应用函数`。比如说，我们固定 `sum` 的第一和第三个参数，定义如下的部分应用函数：

```
scala> val b = sum ( 1 , _ :Int, 3)
b: Int => Int = <function1>

scala> b(2)
res1: Int = 6
```

变量 `b` 的类型为一函数，具体类型为 `function1` （带一个参数的函数），它是由 `sum` 应用了第一个和第三个参数构成的。

调用 `b(2）`，实际上调用 `sum(1, 2, 3)` 。

再比如，我们定义一个新的部分应用函数，只固定中间参数：

```
scala> val c = sum (_:Int, 2, _:Int)
c: (Int, Int) => Int = <function2>

scala> c(1,3)
res2: Int = 6
```

变量 `c` 的类型为 `function2` ，调用 `c(1, 3)` 实际上也是调用 `sum(1, 2, 3)` 。

在 Scala 中，如果你定义一个部分应用函数并且能省去所有参数。比如 `println _` ，你也可以省掉 “`_`” 本身。比如：

```
someNumbers.foreach(println _)
```

可以写成：

```
someNumbers.foreach(println)
```



### 闭包

闭包是一个函数，函数的返回值依赖于函数外部的一个或者多个变量

到目前为止，我们介绍的函数都只引用到传入的参数。假如我们定义如下的函数：

```
(x:Int) => x + more
```

这里我们引入一个自由变量 `more` 。它不是所定义函数的参数，而这个变量定义在函数外面。比如：

```
var more =1
```

那么我们有如下的结果：

```
scala> var more =1
more: Int = 1

scala> val addMore = (x:Int) => x + more
addMore: Int => Int = <function1>

scala> addMore (100)
res1: Int = 101
```

这样定义的函数变量 `addMore` 成为一个“闭包”。因为它引用到函数外面定义的变量。定义这个函数的过程，是将这个自由变量捕获而构成一个封闭的函数。有意思的是，当这个自由变量发生变化时，Scala 的闭包能够捕获到这个变化，因此 Scala 的闭包捕获的是变量本身而不是当时变量的值。

比如：

```
scala> more =  9999
more: Int = 9999

scala> addMore ( 10)
res2: Int = 10009
```

同样的，如果变量在闭包中发生变化，也会反映到函数外面定义的闭包的值。比如：

```
scala> val someNumbers = List ( -11, -10, -5, 0, 5, 10)
someNumbers: List[Int] = List(-11, -10, -5, 0, 5, 10)

scala> var sum =0
sum: Int = 0

scala> someNumbers.foreach ( sum += _)

scala> sum
res4: Int = -11
```

可以看到，在闭包中修改 `sum` 的值，其结果还是传递到闭包的外面。

如果一个闭包所访问的变量有几个不同的版本，比如一个闭包使用了一个函数的局部变量（参数），然后这个函数调用很多次，那么所定义的闭包应该使用所引用的局部变量的哪个版本呢？

简单的说，该闭包定义所引用的变量为定义该闭包时变量的值，也就是定义闭包时相当于保存了当时程序状态的一个快照。比如，我们定义下面一个函数闭包：

```
scala> def makeIncreaser(more:Int) = (x:Int) => x + more
makeIncreaser: (more: Int)Int => Int

scala> val inc1=makeIncreaser(1)
inc1: Int => Int = <function1>

scala> val inc9999=makeIncreaser(9999)
inc9999: Int => Int = <function1>

scala> inc1(10)
res5: Int = 11

scala> inc9999(10)
res6: Int = 10009
```

当你调用 `makeIncreaser(1)` 时，你就创建了一个闭包，该闭包定义的 `more` 的值为 `1` ，而调用 `makeIncreaser(9999)` 所创建的闭包的 `more` 的值为 `9999` 。此后你也无法修改已经返回的闭包的 `more` 的值。因此 `inc1` 始终为加一，而 `inc9999` 始终为加 `9999`。



### 3.7.1 重复参数

scala中使用 *来表明该参数是一个重复参数

例如：

```scala
scala> def echo (args: String *) =
     |   for (arg <- args) println(arg)
echo: (args: String*)Unit

scala> echo()

scala> echo ("One")
One

scala> echo ("Hello","World")
Hello
World
```

在函数内部，变长参数的类型实际上是一个Array，比如上列中的string*类型实际为Array[String]，但是如果传入一个数组类型的参数，是不行的，因为这样是将Array[String]这个整体传给参数，编译器会报错，所以在传入的时候要将该Array解开,在Scala中使用”_*“来解包

#### 3.7.2 命名参数

通常情况下，调用函数时，参数传入和函数定义时参数列表是一一对应的。

```
scala> def  speed(distance: Float, time:Float) :Float = distance/time
speed: (distance: Float, time: Float)Float

scala> speed(100,10)
res0: Float = 10.0
```

使用命名参数时，允许你使用任意顺序传入参数。比如下面的调用：

```
scala> speed( time=10,distance=100)
res1: Float = 10.0

scala> speed(distance=100,time=10)
res2: Float = 10.0
```

#### 3.7.3 缺省参数值

Scala 在定义函数时，允许指定参数的缺省值，从而允许在调用函数时不指明该参数，此时该参数使用缺省值。缺省参数通常配合命名参数使用，例如：

```
scala> def printTime(out:java.io.PrintStream = Console.out, divisor:Int =1 ) =
     | out.println("time = " + System.currentTimeMillis()/divisor)

printTime: (out: java.io.PrintStream, divisor: Int)Unit

scala> printTime()
time = 1383220409463

scala> printTime(divisor=1000)
time = 1383220422
```

#### 柯里化函数

> 柯里化函数是把接受多个参数的函数变换成为接受一个参数(初始函数的一个参数),返回接受余下的参数而且返回结果的新函数的技术。





#### 方法和函数的区别

区别:

1. 方法和函数的定义语法不同
2. 方法一般定义在类，特质，或者object中
3. 方法可以共享类，特质，或者object中的属性
4. 可以调用函数，也可以存放到一个变量中，作为参数传递给其它的方法或者函数中，也可以作为返回值



联系:

1. 可以把函数作为一个参数传递给方法

   ~~~
   scala> val res = (x:Int,y:Int) => x+y
   res: (Int, Int) => Int = $$Lambda$760/1191863711@451882b2
   
   scala> def func(f:(Int,Int)=>Int) = f(5,1)
   func: (f: (Int, Int) => Int)Int
   
   scala> func(res)
   res0: Int = 6
   ~~~

   

2. 方法可以装换成函数

   1. 把一个方法作为参数传递给其它的方法或者函数

      ~~~
      
      scala> def func(f:(Int,Int)=>Int) = f(5,1)
      func: (f: (Int, Int) => Int)Int
      
      scala> func(res)
      res0: Int = 6
      
      scala> def add(x:Int,y:Int) = x+y
      add: (x: Int, y: Int)Int
      
      scala> func(add)
      res1: Int = 6
      ~~~

   2. 通过 空格+下划线把方法转换为函数 

