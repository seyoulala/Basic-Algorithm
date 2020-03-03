# scala 学习笔记(三)

### for表达式

#### 1.枚举元素集合3.4.1 枚举集合元素

这是使用 `for` 表示式的一个基本用法，和 Java 的 `for` 非常类似，比如下面的代码可以枚举当前目录下所有文件：

```
val filesHere = (new java.io.File(".")).listFiles

for(file <-filesHere)
  println(file)
```

![6-3.4.1-1](https://doc.shiyanlou.com/document-uid702660labid6313timestamp1525662101554.png/wm)

其中如 `file <– filesHere` 的语法结构，在 Scala 中称为“生成器 (generator)”。 本例中，`filesHere` 的类型为 `Array[File]`。每次迭代中，变量 `file` 会初始化为该数组中一个元素， `file` 的 `toString()` 为文件的文件名，因此 `println(file)` 打印出文件名。

Scala 的 `for` 表达式支持所有类型的集合，而不仅仅是数组，比如下面使用 `for` 表达式来枚举一个 `Range` 类型。

```
 scala> for(i <- 1 to 4) println("Interation" +i)
Interation 1
Interation 2
Interation 3
Interation 4
```

#### 3.4.2 过滤

某些时候，你可能不想枚举集合中的每一个元素，而是只想迭代某些符合条件的元素。在 Scala 中，你可以为 `for` 表达式添加一个过滤器——在 `for` 的括号内添加一个 `if` 语句，例如：

修改前面枚举文件的例子，改成只列出 `.scala` 文件，示例如下：

```
val filesHere = (new java.io.File(".")).listFiles

for( file <-filesHere
   if file.getName.endsWith(".scala")
)  println(file)
```

如果有必要的话，你可以使用多个过滤器，只要添加多个 if 语句即可。比如，为保证前面列出的文件不是目录，可以添加一个 `if`，如下面代码：

```
val filesHere = (new java.io.File(".")).listFiles

for( file <-filesHere
   if file.isFile
   if file.getName.endsWith(".scala")
)  println(file)
```

#### 3.4.3 嵌套迭代

`for` 表达式支持多重迭代。下面的例子使用两重迭代，外面的循环枚举 `filesHere` ，而内部循环枚举该文件的每一行文字。实现了类似 Unix 中的 `grep` 命令：

```
val filesHere = (new java.io.File(".")).listFiles

def fileLines (file : java.io.File) =
   scala.io.Source.fromFile(file).getLines().toList

def grep (pattern: String) =
  for (
    file <- filesHere if file.getName.endsWith(".scala");
    line <- fileLines(file)
    if line.trim.matches(pattern)
  ) println(file + ":" + line.trim)

grep (".*gcd.*")
```

![6-3.4.3-1](https://doc.shiyanlou.com/document-uid702660labid6313timestamp1525662637076.png/wm)

注意上面代码中，两个迭代之间使用了 `;` ，如果你使用 `{}` 替代 `for` 的 `()` 括号，你可以不使用 `；` 分隔这两个“生成器”。这是因为，Scala 编译器不推算包含在花括号内的省掉的 `;` 。使用 `{}` 改写的代码如下：

```
val filesHere = (new java.io.File(".")).listFiles

def fileLines (file : java.io.File) =
   scala.io.Source.fromFile(file).getLines().toList

def grep (pattern: String) =
  for {
    file <- filesHere if file.getName.endsWith(".scala")
    line <- fileLines(file)
    if line.trim.matches(pattern)
  } println(file + ":" + line.trim)

grep (".*gcd.*")
```

![6-3.4.3-2](https://doc.shiyanlou.com/document-uid702660labid6313timestamp1525662755077.png/wm)

这两段代码是等效的。

#### 3.4.4 绑定中间变量

你可能注意到，前面代码使用了多次 `line.trim` 。如果 `trim` 是个耗时的操作，你可能希望 `trim` 只计算一次。Scala 允许你使用 `=` 号来绑定计算结果到一个新变量。绑定的作用和 `val` 类似，只是不需要使用 `val` 关键字。例如，修改前面的例子，只计算一次 `trim`，把结果保存在 `trimmed` 变量中。

```
val filesHere = (new java.io.File(".")).listFiles

def fileLines (file : java.io.File) =
   scala.io.Source.fromFile(file).getLines().toList

def grep (pattern: String) =
  for {
    file <- filesHere if file.getName.endsWith(".scala")
    line <- fileLines(file)
    trimmed=line.trim
    if trimmed.matches(pattern)
  } println(file + ":" + trimmed)

grep (".*gcd.*")
```

![6-3.4.4-1](https://doc.shiyanlou.com/document-uid702660labid6313timestamp1525663167710.png/wm)

#### 3.4.5 生成新集合

`for` 表达式也可以用来生产新的集合，这是 Scala 的 `for`表达式比 Java 的 `for` 语句功能强大的地方。它的基本语法如下：

```
for clauses yield body
```

关键字 `yield` 放在 body 的前面，`for` 每迭代一次，就产生一个 `body` 。`yield` 收集所有的 `body` 结果，返回一个 `body` 类型的集合