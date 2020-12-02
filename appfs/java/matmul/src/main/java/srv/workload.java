
package srv;

import org.json.simple.JSONObject;

public class workload {

    public workload() {

    }

    private static final int LENGTH = 100;
    
    // matrices multiplication
    public JSONObject handle(JSONObject req) {

        long[][] mat1 = new long[LENGTH][LENGTH];
        long[][] mat2 = new long[LENGTH][LENGTH];
        long[][] prod = new long[LENGTH][LENGTH];

        long factor1 = System.currentTimeMillis() % 24;
        long factor2 = System.currentTimeMillis() % 81;

        for (int i=0; i<LENGTH; i++) {
            for (int j=0; j<LENGTH; j++) {
                mat1[i][j] = (factor1+i)*j;
                mat2[i][j] = i*(factor2-j);
            }
        }

        for(int i = 0; i < LENGTH; i++) {
            for (int j = 0; j < LENGTH; j++) {
                for (int k = 0; k < LENGTH; k++) {
                    prod[i][j] += mat1[i][k] * mat2[k][j];
                }
            }
        }

        long res = 0;
        for (int i=0; i<LENGTH; i++) {
            for (int j=0; j<LENGTH; j++) {
                res += prod[i][j];
            }
        }

        JSONObject response = new JSONObject();
        response.put("label", (char)(res%26+'A'));

        return response;
    }

}
