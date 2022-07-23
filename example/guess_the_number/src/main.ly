import "std/random.ly";
import "std/cmp.ly";

use rand = std::random::rand;

use cmp = std::cmp::cmp;
use Cmp = std::cmp::Cmp;


variant GuessAnswer {
    Guess(u32),
    Quit,
    Err(str),
};


fn guess_answer() {
    fn parse_rec(ans, mul) {
        let c = getc();
        if(c == '0') {
            parse_rec($(ans * 10) + 0);
        }
        elif(c == '1') {
            parse_rec($(ans * 10) + 1);
        }
        elif(c == '2') {
            parse_rec($(ans * 10) + 2);
        }
        elif(c == '3') {
            parse_rec($(ans * 10) + 3);
        }
        elif(c == '4') {
            parse_rec($(ans * 10) + 4);
        }
        elif(c == '5') {
            parse_rec($(ans * 10) + 5);
        }
        elif(c == '6') {
            parse_rec($(ans * 10) + 6);
        }
        elif(c == '7') {
            parse_rec($(ans * 10) + 7);
        }
        elif(c == '8') {
            parse_rec($(ans * 10) + 8);
        }
        elif(c == '9') {
            parse_rec($(ans * 10) + 9);
        }
        else {
            ans;
        };
    };
    print(parse_rec(0));
};


fn main() {
    loop {
        print("Guess the number !");

        let secret : u32 = rand(1:100);

        loop {
            print("Write your guess.");

            let guess : u32 = match(guess_answer()) {
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


guess_answer();
