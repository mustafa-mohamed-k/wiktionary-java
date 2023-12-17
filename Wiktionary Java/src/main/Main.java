
package main;

import com.formdev.flatlaf.FlatLightLaf;

/**
 *
 * @author Mustafa Mohamed
 */
public class Main {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        FlatLightLaf.setup();
        Home home = new Home();
        home.setVisible(true);
    }
    
}
