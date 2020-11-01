package srv;

import org.json.simple.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class workload {

    public workload() {

    }

    public JSONObject handle(JSONObject req) {

        JSONObject response = new JSONObject();

        try {
            String[] cmd = {"bash","-c","LD_LIBRARY_PATH=/srv/tesseract/lib TESSDATA_PREFIX=/srv/tesseract/share/tessdata " +
                    "/srv/tesseract/bin/tesseract /srv/"+req.get("img")+" stdout"};
            Process process = Runtime.getRuntime().exec(cmd);

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            StringBuilder sb = new StringBuilder();
            while ((line = reader.readLine()) != null) {
                sb.append(line);
            }
            int exitVal = process.waitFor();
            assert  exitVal == 0: "Err in executing tesseract";

            response.put("succeed", 1);
            response.put("text", sb.toString());
        }
        catch (Exception e) {
            e.printStackTrace();
            response.put("succeed", 0);
            response.put("error", e.getCause());
        }

        return response;
    }
}
