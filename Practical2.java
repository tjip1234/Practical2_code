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

	static final String TARGET = "HELLO WORLD";
	static final int popSize = 100;
	static final int randompercentage = 20;
	static final int randomnumberrange = 1000;
	static final char[][] selection = new  char[popSize/20][TARGET.length()];
	static char[] alphabet = new char[27];

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
	/**
	 * @param args
	 */
	public static void main(String[] args) {
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
			System.out.println(population[i].genoToPhenotype() +" "+ population[i].getFitness());

		}
		crossover(generator, population);
		for (int i = 0; i < population.length; i++) {
			population[i].setFitness(0.0);
			if (population[i].genoToPhenotype().equals(TARGET)) {
				System.out.println(population[i].genoToPhenotype());
				repeat = false;
			}
		}
		
	}
	

		// do your own cool GA here
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
	
}
