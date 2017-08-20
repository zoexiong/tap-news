/*run in browser*/

var name = 'global';

function Cat() {
   this.name = 'Big C';
   this.foo = function() {
     console.log('foo3', this.name);
   }
   this.bc_foo = this.foo.bind(this);

  /********* 2 **********
  var dog1 = new Dog();
  dog1.fun(cat1.foo);
  dog1.fun(cat1.bc_foo);
  dog1.fun(() => {console.log('匿名', this.name)})
  */
}

cat1 = new Cat();


function Dog() {
   this.name = 'Big D';
   this.fun = function(f) {
     var ff = f;
     ff();
     console.log(this.name);
   }
}

/******** 1 *********/
var dog1 = new Dog();
dog1.fun(cat1.foo);
dog1.fun(cat1.bc_foo);
