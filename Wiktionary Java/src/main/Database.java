package main;

import java.sql.*;

/**
 *
 * @author Mustafa Mohamed
 */
public class Database {

    private static Connection connection;

    public static Connection getConnection() throws SQLException, ClassNotFoundException {
        if (connection == null || connection.isClosed()) {
            // Class.forName("org.sqlite.JDBC");
            String connectionString = "jdbc:sqlite:dictionary.sqlite";
            connection = DriverManager.getConnection(connectionString);
        }
        return connection;
    }
}
