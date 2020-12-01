package srv;

import org.json.simple.JSONObject;

import java.sql.*;

public class workload {

    public workload() {

    }

    private static final int NR_WAREHOUSE = 1;
    private static final int NR_DISTRICT = 10;

    // tpcc stock-level transaction
    public JSONObject handle(JSONObject req) {

        JSONObject response = new JSONObject();

        String host_addr = (String) req.get("host_addr");

        String DB_URL = String.format("jdbc:mysql://%s:3306/tpcc", host_addr);
        String USER = (String) req.get("username");
        String PASS = (String) req.get("password");

        long seed = System.currentTimeMillis();
        int warehouse_id = 1;
        int district_id = (int) ((seed % NR_DISTRICT)+ 1);
        int stock_level = (int) (((seed+29) % 11)+ 10);

        int d_next_o_id = 0;
        int ol_i_id = 0;
        int i_count = 0;

        Connection conn = null;
        Statement stmt = null;
        try {
            // Open a connection
            conn = DriverManager.getConnection(DB_URL,USER,PASS);
            conn.setTransactionIsolation(Connection.TRANSACTION_READ_COMMITTED);
            conn.setAutoCommit(false);

            // Execute the first query
            stmt = conn.createStatement();
            String sql;
            sql = String.format("SELECT d_next_o_id FROM DISTRICT WHERE D_ID = %d AND D_W_ID = %d"
                    , district_id, warehouse_id);
            ResultSet rs = stmt.executeQuery(sql);
            if (rs.next()) {
                d_next_o_id = rs.getInt(1);
            }
            rs.close();

            // Execute the second query
            sql = String.format("SELECT DISTINCT ol_i_id FROM ORDER_LINE WHERE OL_W_ID = %d AND OL_D_ID = %d AND OL_O_ID < %d AND OL_O_ID >= (%d - 20)"
                    , warehouse_id, district_id, d_next_o_id, d_next_o_id);
            rs = stmt.executeQuery(sql);
            while (rs.next()) {
                ol_i_id = rs.getInt(1);
            }
            rs.close();

            // Execute the third query
            sql = String.format("SELECT count(*) FROM STOCK WHERE S_W_ID = %d AND S_I_ID = %d AND S_QUANTITY < %d"
                    , warehouse_id, ol_i_id, stock_level);
            rs = stmt.executeQuery(sql);
            if (rs.next()) {
                i_count = rs.getInt(1);
            }
            rs.close();

            // Commit the transaction
            conn.commit();

            response.put("results", i_count);

            // Clean-up environment
            stmt.close();
            conn.close();
        }
        catch (Exception e) {
            e.printStackTrace();
            try {
		// Cancel the transaction
                conn.rollback();
            }
            catch (SQLException sqle) {
                sqle.printStackTrace();
            }
            response.put("results", "null");
        }
        finally {
            try {
                if(stmt!=null) stmt.close();
                if(conn!=null) conn.close();
            }
            catch (Exception e) {
                System.out.println(e.getCause());
            }
        }

        return response;
    }
}
