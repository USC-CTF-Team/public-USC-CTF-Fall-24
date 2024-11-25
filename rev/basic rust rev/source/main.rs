use std::io;

fn main() {
    let mut in_name = String::new();
    println!("What is your name?");
    io::stdin().read_line(&mut in_name).expect("Error reading name");
    in_name = String::from(in_name.trim());

    let mut in_year = String::new();
    println!("Enter a number.");
    io::stdin().read_line(&mut in_year).expect("Error reading year");

    let year: i32 = in_year.trim().parse().expect("Expected number for year");

    if in_name == "Traveler" && year == 1961 {
        println!("CYBORG{{{}_{}}}", in_name, year);
    } else {
        println!("#{} {}", year, in_name);
    }
}
