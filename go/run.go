package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

// Function to read the content of a file
func readFile(fileName string) (string, error) {
	file, err := os.Open(fileName)
	if err != nil {
		return "", err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	content := ""
	for scanner.Scan() {
		content += scanner.Text() + "\n"
	}
	if err := scanner.Err(); err != nil {
		return "", err
	}
	return content, nil
}

/*
func writeFile(filename string, data string) error {
	// Open the file with write permissions, create it if it doesn't exist
	file, err := os.OpenFile(filename, os.O_WRONLY|os.O_CREATE, 0644)
	if err != nil {
		return err
	}
	defer file.Close()

	// Write the data to the file
	_, err = file.WriteString(data)
	if err != nil {
		return err
	}

	return nil
}
*/

/*
func removePrefix(text, prefix string) string {
	if len(prefix) < len(text) {
		if text[:len(prefix)] == prefix {
			return text[len(prefix):]
		}
	}

	return text
}

func startsWith(text, prefix string) bool {
	if len(prefix) < len(text) {
		if text[:len(prefix)] == prefix {
			return true
		}
	}

	return false
}
*/

func main() {
	//fmt.Println("Hello!"[:1])

	fmt.Println("Go RISCY Interpreter")

	var prevcom string

	scanner := bufio.NewScanner(os.Stdin)
	for {
		fmt.Print("> ")
		scanner.Scan()
		command := scanner.Text()

		if command != "prev" {
			prevcom = command
		}

		if command == "prev" {
			command = prevcom
			fmt.Printf("using command '%s'\n", prevcom)
		}

		switch command {
		case "exit":
			fallthrough
		case "quit":
			fmt.Println("Exiting program...")
			return
		case "help":
			fmt.Println("\n'exit/quit': exits the program\n" +
				"'help': print this message\n" +
				"'run [path]': runs the given file\n" +
				"'compile [path]': compiles the given file into the CRISP format(for more information type 'crisphelp')\n" +
				"'decompile [path]': decompiles the given CRISP file and runs it\n" +
				"'decompile-f [path]': decompiles the given CRISP file and and saves it as a '-decomp.s' file")
		case "crisphelp":
			fmt.Println("\nThe CRISP(no, I'm not British) format is a bytecode format for the RISCPY interpreter.\n" +
				"While yes, it is entirely useless, it does have *some* perks.\n" +
				"It's smaller than a normal .s file because it forfeits all those useless things like 'spaces' and 'comments'(ew)," +
				"\nallowing for less space used.\n\n" +
				"TL;DR, it's like Java bytecode, but it's not Java so it's automatically superior.")
		default:
			if strings.HasPrefix(command, "run ") {
				filepath := command[4:]
				content, err := readFile(filepath)
				if err != nil {
					fmt.Println(err.Error())
					continue
				}
				Interpreter(content)
			} else {
				fmt.Printf("Command '%s' not recognized.\n", strings.Split(command, " ")[0])
			}
		}
	}
}
