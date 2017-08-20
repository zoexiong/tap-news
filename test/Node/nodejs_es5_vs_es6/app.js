import { es6_cube, es6_foo } from './my_modules/es6_module.js';
import es6_module from './my_modules/es6_module.js';

console.log('es6_module: ', es6_module)
console.log(es6_module.es6_cube(6));
console.log(es6_module.es6_foo);

console.log(es6_cube(6));
console.log(es6_foo);



var es5_module = require('./my_modules/es5_module.js')

console.log('es5_module: ', es5_module);
es5_module.default.es5_cube(5);
console.log(es5_module.default.es5_foo);
//
// es5_module.es5_cube(5)
// console.log(es5_module.es5_foo);
