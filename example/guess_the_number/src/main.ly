import "std/random.ly";
import "std/cmp.ly";

use rand = std::random::rand;

use cmp = std::cmp::cmp;
use Cmp = std::cmp::Cmp;


fn main() {
    loop {
        print("Guess the number !");

        let secret = rand(1:100);

        loop {
            print("Write your guess.");

            let guess = match(guess_answer()) {
                Guess(num) => num,
                Quit => return,
                Err(_) => continue,
            };

            print("You guessed ", guess, ".");

            match(cmp(guess, secret)) {
                Cmp(<) => print("Too small !"),
                Cmp(>) => print("Too big !"),
                Cmp(==) => {
                    print("You win !");
                    break;
                },
            };
        };

        print("Continue ? [y/N]");

        match(continue_answer()) {
            Yes => continue,
            * => break,
        };
    };
};

main()
