import java.io.IOException;
import java.io.PrintWriter;
import java.lang.annotation.Target;
import java.util.Arrays;
import java.util.Random;

/**
 * Some very basic stuff to get you started. It shows basically how each
 * chromosome is built.
 * 
 * @author Jo Stevens
 * @version 1.0, 14 Nov 2008
 * 
 * @author Alard Roebroeck
 * @version 1.1, 12 Dec 2012
 * 
 */

public class Practical2 {

	static String TARGET = "HELLO WORLD";
	static int popSize = 1365;
		// do your own cool GA here
	static double randompercentage = 10;
	static final int randomnumberrange = 1000;
	static final char[][] selection = new  char[5][TARGET.length()];
	static char[] alphabet = new char[27];
	static int numberOfItterations = 20;
	static int count = 0;
	// crossover function
	public static void crossover(Random generator, Individual[] population){
		for (int j = 0; j < selection.length; j++) {
			for (int i = 0; i < popSize/selection.length; i++) {
				char[] chromosomereplacement = new char[population[0].getChromosome().length];
				for (int k = 0; k < population[0].getChromosome().length; k++) {
				int select = generator.nextInt(randomnumberrange);
				if (select < (randomnumberrange/2)-((randomnumberrange/100)*randompercentage)) {
					chromosomereplacement[k] = selection[j][k]; 
				} 
				else if (select < (randomnumberrange)-((randomnumberrange/100)*randompercentage)) {
					chromosomereplacement[k] = selection[0][k];
				}
				else {
					chromosomereplacement[k] = alphabet[generator.nextInt(alphabet.length)];
				}
				}
				population[(j+1)*i].setChromosome(chromosomereplacement);
			}
		}
	}
	public static void main(String[] args) throws IOException {
		//fucntion to test the GA 
		//if you don t want this comment the rest and run 
		//mainFunction();

		int rangeOfStringlength = 10;
		String[] endresult = new String[rangeOfStringlength];
		for (int i = 0; i < endresult.length; i++) {
				for (int k = 0; k < numberOfItterations; k++) {
					mainfFunction();
					
				}
				endresult[i] = " "+count/numberOfItterations;
				count = 0;
				
		}
		PrintWriter writer = new PrintWriter("results.csv");
		writer.write(Arrays.toString(endresult));
		writer.println();
		writer.close();
		/**
		 * Some general programming remarks and hints:
		 * - A crucial point is to set each individual's fitness (by the setFitness() method) before sorting. When is an individual fit? 
		 * 	How do you encode that into a double (between 0 and 1)?
		 * - Decide when to stop, that is: when the algorithm has converged. And make sure you  terminate your loop when it does.
		 * - print the whole population after convergence and print the number of generations it took to converge.
		 * - print lots of output (especially if things go wrong).
		 * - work in an orderly and structured fashion (use tabs, use methods,..)
		 * - DONT'T make everything private. This will only complicate things. Keep variables local if possible
		 * - A common error are mistakes against pass-by-reference (this means that you pass the 
		 * 	address of an object, not a copy of the object to the method). There is a deepclone method included in the
		 *  Individual class.Use it!
		 * - You can compare your chromosome and your target string, using for eg. TARGET.charAt(i) == ...
		 * - Check your integers and doubles (eg. don't use ints for double divisions).
		 */
	}
	public static void mainfFunction() throws IOException {
		for (char c = 'A'; c <= 'Z'; c++) {
			alphabet[c - 'A'] = c;
		}
		alphabet[26] = ' ';
		Random generator = new Random(System.currentTimeMillis());
		Individual[] population = new Individual[popSize];
		// we initialize the population with random characters
		for (int i = 0; i < popSize; i++) {
			char[] tempChromosome = new char[TARGET.length()];
			for (int j = 0; j < TARGET.length(); j++) {
				tempChromosome[j] = alphabet[generator.nextInt(alphabet.length)]; //choose a random letter in the alphabet
			}
			population[i] = new Individual(tempChromosome);
		}
		boolean repeat = true;
		while (repeat) {
		for (int i = 0; i < population.length; i++) {
			for (int j = 0; j < TARGET.length(); j++) {
				char compare = population[i].genoToPhenotype().charAt(j);
				char comparetarget = TARGET.charAt(j);
				if ( compare == comparetarget) {
					population[i].setFitness(population[i].getFitness() + (1.0/TARGET.length()));
				}
			}
		}
		HeapSort.sort(population);
		for (int i = 0; i < selection.length; i++) {
			selection[i] = population[i].getChromosome();
		}
		// What does your population look like?
		for (int i = 0; i < population.length; i++) {
			//System.out.println(population[i].genoToPhenotype() +" "+ population[i].getFitness());

		}
		//randompercentage = (1.0/population[0].getFitness());
		double x = TARGET.length()*population[0].getFitness(); // adaptive mutation rate 
		crossover(generator, population);
		for (int i = 0; i < population.length; i++) {
			population[i].setFitness(0.0);
			if (population[i].genoToPhenotype().equals(TARGET)) {
				//System.out.println(population[i].genoToPhenotype());
				repeat = false;
			}
		}
		count++;
		randompercentage = ((15/x)-Math.log(x))+7.8; // adaptive mutation rate calculation
		System.out.println(randompercentage);
	}
	System.out.println(count);
	}
	
}
