var es5_cube = function(x) {
  console.log('es5 cude: x =', x);
  return x * x * x;
}
// module.exports = es5_cube;

var es5_foo = Math.PI + Math.SQRT2;
// module.exports = es5_foo;

exports.default = { es5_cube, es5_foo };
