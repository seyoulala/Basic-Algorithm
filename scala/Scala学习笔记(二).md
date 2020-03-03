# Scala学习笔记(二)

### 类和对象

首先介绍 Scala 的类定义，我们以一个简单的例子开始，创建一个计算整数累计校验和的类 `ChecksumAccumulator` 。

```scala
class ChecksumAccumulator{
   private var sum=0
   def add(b:Byte) :Unit = sum +=b
   def checksum() : Int = ~ (sum & 0xFF) +1
}
```

![3-3.1-1](https://doc.shiyanlou.com/document-uid702660labid6310timestamp1525425822990.png/wm)

可以看到 Scala 类定义和 Java 非常类似，也是以 `class` 开始，和 Java 不同的，Scala 的缺省修饰符为`public`，也就是如果不带有访问范围的修饰符 `public` 、`protected`、`private` 等，Scala 将默认定义为 `public` 。类的方法以 `def` 定义开始，要注意的是Scala的方法的参数都是 `val`类型，而不是 `var` 类型，因此在函数体内不可以修改参数的值，比如：如果你修改 `add` 方法如下：

```scala
def add(b:Byte) :Unit ={
      b=1
      sum+=b
  }
```

此时编译器会报错：

![3-3.1-2](https://doc.shiyanlou.com/document-uid702660labid6310timestamp1525425844215.png/wm)

类的方法分两种，一种是有返回值的，一种是不含返回值的，没有返回值的主要是利用代码的“副作用”，比如修改类的成员变量的值或者读写文件等。Scala 内部其实将这种函数的返回值定为 `Unit`（类同 Java 的 void 类型），对于这种类型的方法，可以省略掉 `=` 号，因此如果你希望函数返回某个值，但忘了方法定义中的 `=`，Scala 会忽略方法的返回值，而返回 `Unit` 。

再强调一下，Scala 代码无需使用 `；` 结尾，也不需要使用 `return` 返回值，函数的最后一行的值就作为函数的返回值。

但如果你需要在一行中书写多个语句，此时需要使用 `；` 隔开，不过不建议这么做。你也可以把一条语句分成几行书写，Scala 编译器大部分情况下会推算出语句的结尾，不过这样也不是一个好的编码习惯。



### 对象

Scala 比 Java 更加面向对象，这是因为 Scala 不允许类保护静态元素(静态变量或静态方法）。在 Scala 中提供类似功能的是称为“ `Singleton`（单例对象）”的对象。在 Scala 中定义 `Singleton` 对象的方法，除了使用 `object` 而非 `class` 关键字外，其它方式和类定义非常类似。下面例子创建一个 `ChecksumAccumulator` 对象：

```
object ChecksumAccumulator {
   private val cache = Map [String, Int] ()
   def calculate(s:String) : Int =
      if(cache.contains(s))
         cache(s)
      else {
         val acc=new ChecksumAccumulator
         for( c <- s)
            acc.add(c.toByte)
         val cs=acc.checksum()
         cache += ( s -> cs)
         cs
       }
}
```

这个对象和上一个创建的类 `ChecksumAccumulator` 同名，这在 Scala 中把这个对象称为其同名的类的“伴侣”对象（Companion object)。 如果你需要定义类的 `companion` 对象，Scala 要求你把这两个定义放在同一个文件中。类和其 companion 对象可以互相访问对方的私有成员。

如果你是 Java 程序员，可以把 `Singleton` 对象看成以前 Java 定义静态成员的地方。你可以使用类似 Java 静态方法的方式调用 `Singleton` 对象的方法，比如下面为这个例子完整的代码：

```
import scala.collection.mutable.Map

class ChecksumAccumulator{
   private var sum=0
   def add(b:Byte) :Unit = sum +=b
   def checksum() : Int = ~ (sum & 0xFF) +1
}

object ChecksumAccumulator {
   private val cache = Map [String, Int] ()
   def calculate(s:String) : Int =
      if(cache.contains(s))
         cache(s)
      else {
         val acc=new ChecksumAccumulator
         for( c <- s)
            acc.add(c.toByte)
         val cs=acc.checksum()
         cache += ( s -> cs)
         cs
       }
}

println ( ChecksumAccumulator.calculate("Welcome to Scala Chinese community"))
```

![3-3.2-1](https://doc.shiyanlou.com/document-uid702660labid6310timestamp1525426620973.png/wm)

Scala 的 `singleton` 对象不仅仅局限于作为静态对象的容器，它在 Scala 中也是头等公民，但仅仅定义 `Singleton` 对象本身不会创建一个新的类型，你不可以使用 `new` 再创建一个新的 `Singleton` 对象（这也是 Singleton 名字的由来），此外和类定义不同的是，`singleton` 对象不可以带参数（类定义参数将在后面的内容中介绍）。

回过头来看看我们的第一个例子 “Hello World” 。

```
object HelloWorld {
  def main(args: Array[String]) {
    println("Hello, world!")
  }
}
```

这是一个最简单的 Scala 程序，`HelloWorld` 是一个 `Singleton` 对象，它包含一个 `main` 方法（可以支持命令行参数）。和 Java 类似， Scala 中任何 `Singleton` 对象，如果包含 `main` 方法，都可以作为应用的入口点。

在这里要说明一点的是，在 Scala 中不要求 `public` 类定义和其文件名同名，不过使用 `public` 类和文件同名还是有它的优点的，你可以根据个人喜好决定是否遵循 Java 文件命名风格。

最后提一下 Scala 的 `Trait` 功能，Scala 的 `Trait` 和 Java 的 `Interface` 相比，可以有方法的实现（这点有点像抽象类，但如果是抽象类，就不会允许继承多个抽象类）。Scala 的 `Trait` 支持类和 `Singleton` 对象以及多个 `Trait` 混合（使用来自这些 `Trait` 中的方法，而不是不违反单一继承的原则）。