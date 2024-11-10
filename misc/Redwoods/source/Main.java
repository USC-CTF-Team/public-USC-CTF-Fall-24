import java.util.Scanner;

public class Main {
    static String[] flags = new String[] {
            "ccccccccccagccccccchdbgdddehcccccagcccchdbgccehcccccagddddhdbgdddehgcccccccccccccecccedddddddd",
            "dddeagcgchhdbcccccagcccccccccchdbgccegcedddeddddeccccccccccccccccceddddddddddddddehhccccccaggccccchhdbggdddeddddddddddde",
            "ddehhccccccaggdddddhhdbggdeehhcccccccccccaggcccchhdbggehhcccccaggdddddhhdbggeagcgchhdbabccccccaggdddhhdbggehcccccceehhcce"
    };
    static Scanner sc;
    static boolean animalSpeaking = false;
    public static void main(String[] args) {
        sc = new Scanner(System.in);

        System.out.println("You are wandering through the woods to clear your mind, escape the concrete barriers of the modern world, and find enlightenment in what is known as a flag.");
        System.out.println();
        int location = 0;
        int trailMix = 3;

        boolean[] visited = new boolean[10];

        while (true) {
            int enterLoc = location;
            if (location == 0) {
                if (!visited[0])
                    System.out.println("You come across a climbable tree, but could also simply continue further.");
                else
                    System.out.println("You are at the base of the tree, and see a route leading into the depths of the forest.");
                int c = getChoice("Climb the tree", "Venture further", "Leave");
                switch (c)
                {
                    case 1:
                        location = 1; break;
                    case 2:
                        location = 2; break;
                    case 3:
                        System.exit(0); break;
                }
            }
            else if (location == 1) {
                if (!visited[3]) {
                    System.out.println("You find a comfortable spot on the tree branch and look out towards the horizon. " +
                            "It is beautiful in a way that could not be described fully in text... if only there were a picture that showed what this forest looked like.");
                    System.out.println("But your imagination is powerful, and your spirit is warmed.");
                }
                int c = getChoice("Press F5", "Climb down");
                location = c == 1 ? 3 : 0;
            } else if (location == 2) {
                if (!visited[2]) {
                    System.out.println("You venture into the forest, pushing past bushes and branches to uncover more trees and animals around you.");
                    System.out.println("A squirrel hops out of a bush and is scuttling around in front of you.");
                }
                else if (trailMix == 3){
                    System.out.println("The squirrel is still there, presumably searching for food.");
                }
                else {
                    System.out.println("The squirrel is still there, nibbling on its trail mix.");
                }
                int c;
                if (trailMix == 3)
                    c = getChoice("Offer the squirrel trail mix", "Punt the squirrel", "Ignore the squirrel and continue", "Go back");
                else
                    c = getChoice("Offer the squirrel trail mix", "Punt the squirrel", "Continue deeper into the forest", "Go back");
                location = switch (c) {
                    case 1 -> 4;
                    case 2 -> 5;
                    case 3 -> 6;
                    case 4 -> 0;
                    default -> location;
                };
            } else if (location == 3) {
                System.out.println("You pressed F5 and gained a whole new perspective.");
                if (!animalSpeaking)
                    System.out.println("You can feel the voices of the forest connecting with your soul.");
                animalSpeaking = true;
                location = 1;
            } else if (location == 4) {
                if (trailMix > 0)
                {
                    trailMix--;
                    System.out.println("The squirrel looks up at you and happily accepts the nuts you hand out.");
                    if (animalSpeaking) {
                        System.out.println("The squirrel utters the following phrase:");
                        System.out.println(flags[3 - (trailMix+1)]);
                    }
                    else {
                        System.out.println("The squirrel utters an unintelligible but cute sound.");
                    }
                    System.out.println("You have " + trailMix + " trail mix remaining.");
                    if (trailMix == 2)
                        System.out.println("The squirrel looks like it is very hungry.");
                    else if (trailMix == 1)
                        System.out.println("The squirrel looks like it is still hungry.");
                }
                else
                {
                    System.out.println("You have no trail mix left. ");
                }
                location = 2;
            } else if (location == 5) {
                System.out.println("You swing your leg back, then swing forward with all your might and punt the squirrel into forest oblivion.");
                System.out.println("Your meditative adventure has made you realize you are a terrible person, so you leave the forest and return to society.");
                System.exit(0);
            } else if (location == 6) {
                System.out.println("You walk past the squirrel and journey deeper and deeper into the forest.");
                if (trailMix == 3) {
                    System.out.println("You have a nagging feeling that you missed something along the way, that valuable lessons were not extracted.");
                    System.out.println("But you push on anyways, consuming yourself within the misty woods.");
                }
                else if (!animalSpeaking)
                {
                    System.out.println("You feel comforted by your interaction with the squirrel, but something tells you that you did not fully understand what it was trying to say.");
                    System.out.println("Perhaps another journey through the forest would give you a new perspective.");
                    System.out.println("But for now, you venture deeper, consuming yourself within the misty woods.");
                }
                else
                {
                    System.out.println("You feel enlightened by your connection to nature.");
                    System.out.println("You are ready to continue further, but you must dig deeper in a way that cannot be accomplished in this text adventure.");
                }
                System.exit(0);
            }
            System.out.println();
            visited[enterLoc] = true;
        }
    }

    public static int getChoice(String... options)
    {
        for (int i = 0; i < options.length; i++)
        {
            System.out.println((i+1) + ": " + options[i]);
        }
        System.out.println("Enter a number: ");
        int choice = sc.nextInt();
        if (choice < 1 || choice > options.length)
        {
            System.out.println("You are trying to do something you are not capable of.");
            return getChoice(options);
        }
        return choice;
    }
}