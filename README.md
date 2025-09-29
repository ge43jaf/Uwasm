# Uwasm -- An interpreter for Wasm

Mainly focus on the imlementation of key functions using the Wasm textual format

### Flow diagram for Uwasm
![](/images/Uwasm_flow_diagram.png)


## How to Use It

Uwasm provides a command-line interface for executing WebAssembly modules written in the WAT. Its design emphasizes ease of integration, validation, and debugging. Below are the key usage scenarios.

#### Installation \& Setup
Uwasm requires Python 3.8+ and no external dependencies beyond the standard library. Clone the repository and navigate to the project directory:

```
            git clone https://github.com/ge43jaf/Uwasm
            cd src/python_scripts/
```

To verify installation, run the following command to evoke the helper page:

```
            python main.py -h
```

You can also run the test suite using the **-t** flag:

```
            python main.py -t
```

This executes all test cases in **../tests/success** and **../tests/failure**, performing lexical analysis, parsing, and automatic validation. 


#### Running WebAssembly Modules

To execute a WAT file, use the **--ast** flag to generate the abstract syntax tree:

```
            python main.py --ast input.wat
```


#### Command-line API
Uwasm is a command-line program that supports the following arguments, implemented via Python's **argparse** (see **main.py**):

    -h, --help: Shows the help message.
    -t, --test: Executes all test cases.
    -a, --ast: Outputs the AST for a given WAT file.
    -d, --debug: Enables verbose logging (planned feature).
    -v, --validate: Validate the programm based on the generated AST.
    -b, --branch: Generate AST with branch structure.
    -c, --color: Generate AST with branch and colorized keywords.
    -i, --interpret:       Interpret the WebAssembly program.
    -F FUNCTION, --function FUNCTION:       Pass name of the function to execute.
    -p PARAMS, --params PARAMS:  Pass function parameters as a string array, e.g. ``1 2 3''.



When run on the following **module** containing a function **\$add**, Uwasm would produce
one of the abstract syntax trees shown in Figure~\ref{fig:awesome_image1}, Figure~\ref{fig:awesome_image2}, and Figure~\ref {fig:awesome_image3}, depending on the provided command-line arguments. The space in Figure~\ref{fig:awesome_image1} between **Module** and **Func** is a placeholder for **Memory**, which in this example does not exist.

```
            (module
                (func $add (param $a i32) (param $b i32) (result i32)
                    (local.get $a)
                    (local.get $b)
                    (i32.add)
                )
            )
```

AST generated when using the **-a** flag             |  AST generated when using the **-b** flag  | AST generated when using the **-c** flag 
:-------------------------:|:-------------------------:|:---
![](/images/--a.png)  |  ![](/images/--b.png) | ![](/images/--c.png)




