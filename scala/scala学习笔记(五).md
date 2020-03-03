## scala学习笔记

### java中修饰符

*被修饰符修饰的属性或者方法的作用域*

|           | 当前类 | 同一个包内 | 子类   | 其它包 |
| :-------- | ------ | ---------- | ------ | ------ |
| public    | 可见   | 可见       | 可见   | 可见   |
| Protected | 可见   | 可见       | 可见   | 不可见 |
| (default) | 可见   | 可见       | 不可见 | 不可见 |
| Private   | 可见   | 不可见     | 不可见 | 不可见 |

### scala中定义类

~~~
//val 修饰的属性，系统会自动生成get方法
//var 修饰的属性，系统会自动生成get和set方法
//private var 修饰的属性，系统会自动生成private修饰的get和set方法
//private[this]修饰的属性，系统不会生成get和set方法
//同时只有当前对象可以访问该属性

class person {
    var age = 10
    //定义一个辅助构造函数
    def this(age1:Int) = {
        //首先调用主构造函数或者其它辅助构造函数
        this()
        this.age = age1
    }
    //主构造函数中定义的所有语句都会被执行
    println("hello scala")

}

object test{
    def main(args: Array[String]): Unit = {
       var per = new person(100)
       println(per.age)
        
    }
}

~~~

 ### 单例对象

`object`在scala中称为单例对象,看成工具类，里面可以定义工具函数和常量 

~~~
import java.io.File
import collection.mutable.{ListBuffer,ArrayBuffer}
//定义一个单例对象,相当于一个工具类，里面可以存放工具方法和常量，方法可以通过类名.方法名进行调用
//单例对象不能带参数

object Hello {
    def log(msg:String) = {
        println(s"Info:$msg")
    }
}
class  Test {
    def  method = {
        Hello.log("hello")
    }

}

//再定义一个单例对象来调用这些方法
object testlog{
    def main(args: Array[String]): Unit = {
        Hello.log("world")
        val obj:Test = new  Test
        println(obj.method)
    }

}
~~~



### 伴生对象和伴生类

伴生对象和伴生类可以互相调用各自的私有方法或者属性

~~~
class  Test {
//调用伴生对象中的私有方法和私有属性
   val res = Test.method 

}

//再定义一个单例对象来调用这些方法
object Test{
    private  var lastnumber = 0
    private  def method = {
        lastnumber+=1
        lastnumber
    }

}
~~~

### apply方法unapply方法

```

//带有参数的主构造函数
class  Test( val user:String,val passwd:String) {

}

//再定义一个单例对象来调用这些方法
object Test {
    //使用apply方法来创建一个对象
    def apply(user: String, passwd: String): Test = new Test(user, passwd)

    //定义一个unapply方法来提取对象中的参数
    def unapply(arg: Test): Option[(String, String)] = {
        if (arg == null) None
        else {
            Some(arg.user,arg.passwd)
        }
    }
}

//应用程序对象
object  maintest extends  App{
    //使用伴生对象的apply方法来创建一个对象
    var obj:Test = Test("hello","world")
    //使用new来创建一个对象
    var obj2 = new Test("你好","hao")
    //对obj对象进行模糊匹配
    obj match {
        case Test(user,password) => println(user+":"+password)
        case _ => println("none")

    }

}
```

### 继承需要注意的点

```
class person(val dx:Int,val dy:Int) {
    var x:Int =dx
    var y:Int = dy
    def move(move_x:Int,move_y:Int) = {
        x+=move_x
        y+=move_y
        println(x,y)
    }
}

//写一个person的子类
//子类继承了父类的所有属性和方法
//重写父类的非抽象方法需要使用overwrite
//重写父类的抽象方法，overwrite可要可不要
//final修饰的类，方法，属性不能重写
class subperson(override val dx:Int,override val dy:Int,val dz:Int) extends person(dx,dy){
    var z:Int = dz
    def move(move_x:Int,move_y:Int,monv_z:Int) =
        {
            x+=move_x
            y+=move_y
            z+=monv_z
            println(x,y,z)
        }
}

object test{
    def main(args: Array[String]): Unit = {
       val  obj:subperson = new subperson(1,2,3)
        obj.move(2,3,4)
    }
}
```

### 抽象类

抽象类被`abstract`修饰，定义的属性可以没有初始值，同时方法也可以没有方法体，但是也可以定义有方法体的方法。

```
abstract  class person {
    var id:Int
    def method(x:Int,y:Int):Int
    def hello(S:String) = {
        println(s"hello world $S")
    }

}

//写一个类继承抽象类，定义其中的变量以及方法，同时重写其中的hello方法
class  subperson extends person{
    override var id: Int = 10
    override def method(x: Int, y: Int): Int = {
       val  dx = 10*x
       val  dy = 10*y
        dx+dy
    }

    override def hello(S: String): Unit = {
        println(s"This is overwrite methon $S")
    }

}
```

### 模式匹配

1.通配符匹配

2.常量字面值匹配

3.常量变量匹配



```
object match_object {
    def main(args: Array[String]): Unit = {
        val res = "nihaoa"
        //使用match进行模式匹配
        val RES = "nihaoa"
        //通配符匹配
        val list1 = List(1,2,3)
        res match {
            //常量字面值匹配
//            case "nihaoa" => println("success")
            //常量变量匹配，注意要使用大写
            case  RES => println("succsee")
            case _ => println("fail")
        }

        list1 match {
            // 使用_ 来表示通配符，如果是相同的结构，那么匹配就会成功
            case  List(_,_,3) => println("success")
            case _ => println("fail")
        }
    }
}

```



### 高阶函数

参数是一个函数，返回值也是一个函数，或者参数和返回值都是一个函数





