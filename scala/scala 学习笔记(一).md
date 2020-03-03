

# scala 学习笔记(一)

### Array，List,Set,map等数据类型的使用

数组Array在scala中是可以进行修改的,但是List对象不可修改，

```scala
val oneTwo = List(1,2)
val threeFour = List(3,4)
val oneTwoThreeFour=oneTwo ::: threeFour
println (oneTwo + " and " + threeFour + " were not mutated.")
println ("Thus, " + oneTwoThreeFour + " is a new list")
```

通过创建两个List对象，然后通过:::操作符来讲两个List进行连接,同时提供::操作符向List中添加元素。List提供以下几个方法`head,tail,reverse,length,last`等

~~~

~~~







set在scala中分为两种类型，缺省情况 `Set` 为 `Immutable Set`，如果你需要使用可修改的集合类（ `Set` 类型），你可以使用全路径来指明 `Set` ，比如 `scala.collection.mutable.Set` 。

Scala 提供的另外一个类型为 `Map` 类型，Map(映射)是一种可迭代的key/value结构，所有的值都可以通过键来获取。 Scala 也提供了 `Mutable` 和 `Immutable` 两种 Map 类型，如下图所示。

![2-3.9-3](https://doc.shiyanlou.com/document-uid162034labid1679timestamp1453868227251.png/wm)

Map 的基本用法如下（Map 类似于其它语言中的关联数组，如 PHP ）,默认是不可修改的

```scala
val romanNumeral = Map ( 1 -> "I" , 2 -> "II",
  3 -> "III", 4 -> "IV", 5 -> "V")
```



#### 简单判断指令编程和函数编程

一个简单的原则，如果代码中含有 `var` 类型的变量，这段代码就是传统的指令式编程，如果代码只有 `val` 变量，这段代码就很有可能是函数式代码，因此学会函数式编程关键是不使用 `vars` 来编写代码。

来看一个简单的例子：

```
def printArgs ( args: Array[String]) : Unit ={
    var i=0
    while (i < args.length) {
      println (args(i))
      i+=1
    }
}
```

来自 Java 背景的程序员开始写 Scala 代码很有可能写成上面的实现。我们试着去除 `vars` 变量，可以写成更符合函数式编程的代码：

```
def printArgs ( args: Array[String]) : Unit ={
    for( arg <- args)
      println(arg)
}
```

![2-3.10-1](https://doc.shiyanlou.com/document-uid702660labid6308timestamp1525424671068.png/wm)

或者更简化为：

```
def printArgs ( args: Array[String]) : Unit ={
    args.foreach(println)
}
```

![2-3.10-2](https://doc.shiyanlou.com/document-uid702660labid6308timestamp1525424683170.png/wm)

这个例子也说明了尽量少用 `vars` 的好处，代码更简洁明了，从而也可以减少错误的发生。因此 Scala 编程的一个基本原则是，能不用 `vars`，尽量不用 `vars`，能不用 `mutable` 变量，尽量不用 `mutable` 变量，能避免函数的副作用，就尽量不产生副作用。

#### 读写文件

使用脚本实现某个任务，通常需要读取文件，本节介绍 Scala 读写文件的基本方法。比如下面的例子读取文件的每行，把该行字符长度添加到行首：

```
import scala.io.Source

var args=Source.fromFile("/home/hadoop/test.txt") #记得在对应目录创建test.txt 文件，并写入一些内容

for( line <- args.getLines)
    println(line.length + "" + line)
```

![2-3.11-1](https://doc.shiyanlou.com/document-uid702660labid6308timestamp1525424968852.png/wm) 可以看到 Scala 引入包的方式和 Java 类似，也是通过 `import` 语句。文件相关的类定义在 `scala.io` 包中。 如果需要引入多个类， Scala 使用 `_` 而非 `*`。



#### 什么是集合?

集合是存储各种数据类型对象的一个容器

不可变集合：不可修改,但是可以模拟修改或者删除操作等

可变集合:可修改，可以更新或者扩充

