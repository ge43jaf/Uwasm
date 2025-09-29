# Uwasm -- An interpreter for Wasm

Mainly focus on the imlementation of key functions using the Wasm textual format

### Flow diagram for Uwasm
![](/images/Uwasm_flow_diagram.png)


\subsection{How to Use It}
\label{subsec:usage}

Uwasm provides a command-line interface for executing WebAssembly modules written in the WAT. Its design emphasizes ease of integration, validation, and debugging.
% , following the WebAssembly specification~\cite{WebAssemblySpec2025}. 
Below are the key usage scenarios.

\subsubsection{Installation \& Setup}
Uwasm requires Python 3.8+
% ----\\
% (TODO)
% ----
and no external dependencies beyond the standard library. Clone the repository and navigate to the project directory:

\begin{verbatim}
            git clone https://github.com/ge43jaf/Uwasm
            cd src/python_scripts/
\end{verbatim}

To verify installation, run the following command to evoke the helper page:
\begin{verbatim}
            python main.py -h
\end{verbatim}

You can also run the test suite using the \texttt{-t} flag:
% (Figure~\ref{fig:cli-test}):
\begin{verbatim}
            python main.py -t
\end{verbatim}

This executes all test cases in \texttt{../tests/success} and \texttt{../tests/failure}, performing lexical analysis, parsing, and automatic validation. 
% The test framework adheres to the WebAssembly test suite structure~\cite{Rossberg2017}.

\subsubsection{Running WebAssembly Modules}

% ----\\
% TODO
% ----

To execute a WAT file, use the \texttt{--ast} flag to generate the abstract syntax tree:

\begin{verbatim}
            python main.py --ast input.wat
\end{verbatim}

The abstract syntax tree generation process handles the module in three phases:
\begin{enumerate}
    \item \textbf{Lexical Analysis:} Tokenizes input using regular expressions (see \texttt{Lexer.py}).
    \item \textbf{Parsing:} Constructs an AST via recursive descent parsing (\texttt{Parser.py}).
    \item \textbf{Validation:} Performs type checking, export validation, and stack simulation (\texttt{Validator.py}).
\end{enumerate}




% \caption{Example WAT module with a function adding two integers.}
% \label{lst:wat-example}
% \end{listing}

\subsubsection{Command-line API}
Uwasm is a command-line program that supports the following arguments, implemented via Python's \texttt{argparse} (see \texttt{main.py}):
\begin{itemize}
    % \item \texttt{-h, -{}-help}: Shows the help message.
    \item \texttt{-t, -{}-test}: Executes all test cases.
    \item \texttt{-a, -{}-ast}: Outputs the AST for a given WAT file.
    \item \texttt{-d, -{}-debug}: Enables verbose logging (planned feature).
    \item \texttt{-v, -{}-validate}: Validate the programm based on the generated AST.
    \item \texttt{-b, -{}-branch}: Generate AST with branch structure.
    \item \texttt{-c, -{}-color}: Generate AST with branch and colorized keywords.
    \item  \texttt{-i, --interpret}:       Interpret the WebAssembly program.
    \item  \texttt{-F FUNCTION, --function FUNCTION}:       Pass name of the function to execute.
    \item  \texttt{-p PARAMS, --params PARAMS}:  Pass function parameters as a string array, e.g. ``1 2 3''.
\end{itemize}


% For example, the following \texttt{module} contains a function \texttt{\$add}
% % ~\ref{lst:wat-example}
% would produce

When run on the following \texttt{module} containing a function \texttt{\$add}, Uwasm would produce
one of the abstract syntax trees shown in Figure~\ref{fig:awesome_image1}, Figure~\ref{fig:awesome_image2}, and Figure~\ref {fig:awesome_image3}, depending on the provided command-line arguments. The space in Figure~\ref{fig:awesome_image1} between \texttt{Module} and \texttt{Func} is a placeholder for \texttt{Memory}, which in this example does not exist.
% ~\ref{fig:ast-output}.

% \begin{listing}[htbp]
\begin{verbatim}
            (module
                (func $add (param $a i32) (param $b i32) (result i32)
                    (local.get $a)
                    (local.get $b)
                    (i32.add)
                )
            )
\end{verbatim}


% \begin{figure}[H]
%     \centering
%     \includegraphics[width=0.3\linewidth]{images/--a.png}
%     \caption{AST generated with -a flag}
%     \label{fig:placeholder}
% \end{figure}

% \begin{figure}[H]
%     \centering
%     \includegraphics[width=0.3\linewidth]{images/--b.png}
%     \caption{AST generated with -b flag}
%     \label{fig:placeholder}
% \end{figure}

% \begin{figure}[H]
%     \centering
%     \includegraphics[width=0.3\linewidth]{images/--c.png}
%     \caption{AST generated with -c flag}
%     \label{fig:placeholder}
% \end{figure}

\begin{figure}[H]
\minipage{0.32\textwidth}
  \includegraphics[width=\linewidth]{images/--a.png}
  \caption{AST generated when using the \texttt{-a} flag}\label{fig:awesome_image1}
\endminipage\hfill
\minipage{0.32\textwidth}
  \includegraphics[width=\linewidth]{images/--b.png}
  \caption{AST generated when using the \texttt{-b} flag}\label{fig:awesome_image2}
\endminipage\hfill
\minipage{0.32\textwidth}%
  \includegraphics[width=\linewidth]{images/--c.png}
  \caption{AST generated when using the \texttt{-c} flag}\label{fig:awesome_image3}
\endminipage
\end{figure}
