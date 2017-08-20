

var a = 37;

var obj1 = {
   a: 39,
   //f: () => {
   f: function() {
      console.log(this.a);
   }
}

obj1.f();

var out_f = obj1.f;
out_f();

var obj2 = {
   a: 40,
   f: function(callback) {
      // g = callback.bind(this)
      // g();
      callback();
   }
}

obj2.f(obj1.f);
