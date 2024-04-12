``` 
 ______ _ _      _    _                       
|  ____| (_)    | |  | |                      
| |__  | |_  ___| | _| |     __ _ _ __   __ _ 
|  __| | | |/ __| |/ / |    / _` | '_ \ / _` |
| |    | | | (__|   <| |___| (_| | | | | (_| |
|_|    |_|_|\___|_|\_\______\__,_|_| |_|\__, |
                                         __/ |
                                        |___/ 
```
# FlickLang

FlickLang is a simple, interpreted programming language designed for educational purposes and to demonstrate fundamental programming language concepts. It features variable assignment, basic arithmetic, conditionals, loops, arrays, and printing capabilities.

## Features

- **Basic Arithmetic:** FlickLang supports arithmetic operations such as addition, subtraction, multiplication, and division.

- **Variables:** You can declare and use variables in FlickLang to store and manipulate data.

- **Comments:** FlickLang supports single-line comments starting with `..`, allowing you to add explanatory notes in your code.

- **Strings:** Strings in FlickLang are written with single quotes `'`.

- **Printing to a Console:** FlickLang allows you to print messages to the console using the `p` keyword, followed by a string enclosed in single quotes `'`.

- **Arrays:** FlickLang supports the creation and manipulation of arrays. Arrays are defined using square brackets [] and can contain numbers, strings, or other arrays. Elements within an array can be accessed and assigned using indexing, which starts at 0.

- **Loops:**  FlickLang currently supports while loops for performing repetitive tasks. The syntax for a while loop starts with the keyword w, followed by a condition, and a block of statements in curly braces {} to execute as long as the condition evaluates to true.

## Usage
To run a FlickLang script, use the following command:

```bash
poetry run flicklang path_to_flicklang_script
```

FlickLang can also be used in interpreted mode if no script is provided, allowing for interactive execution of commands:

```bash
poetry run flicklang
```

## Example
Here's an example of a simple FlickLang program that calculates the area of a rectangle:

```FlickLang
.. Calculate the area of a rectangle
length = 10
width = 5
area = length * width
p 'The area of the rectangle is: ', area
```

### More Examples

**Variable Assignment and Arithmetic**
```FlickLang
a = 10 b = a + 5 p b .. Prints 15
```

**Conditionals**
```FlickLang
a = 10 if a eq 10 { p 'a is 10' } el { p 'a is not 10' }
```

**While Loop**
```FlickLang
a = 0 w (a ls 5) { p a a = a + 1 }
```

**Array and Indexing**
```FlickLang
a = [1, 2, 3, 4, 5] a[2] = 10 p a[2] .. Prints 10
```