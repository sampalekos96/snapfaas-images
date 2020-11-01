package srv;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import org.im4java.core.ConvertCmd;
import org.im4java.core.IMOperation;

import java.io.File;
import java.io.FileInputStream;
import java.util.Base64;

public class workload {

    public workload() {

    }

    public JSONObject handle(JSONObject req) {

        JSONObject response = new JSONObject();

        String imageName = "/srv/"+req.get("img");
        String thumbnailName = "/run/thumbnail.jpg";
        JSONArray jArray = (JSONArray) req.get("size");
        int width = ((Long)jArray.get(0)).intValue();
        int height = ((Long)jArray.get(0)).intValue();

        ConvertCmd cmd = new ConvertCmd();
        IMOperation op = new IMOperation();

        op.addImage(imageName);
        op.resize(width, height);
        op.addImage(thumbnailName);

        try {
            cmd.setSearchPath("/srv/bin");
            cmd.run(op);

            File thumbnailFile = new File(thumbnailName);
            FileInputStream fileInputStreamReader = new FileInputStream(thumbnailFile);
            byte[] bytes = new byte[(int)thumbnailFile.length()];
            fileInputStreamReader.read(bytes);

            String imageString = Base64.getEncoder().encodeToString(bytes);
            response.put("serialized_img", imageString);
        }
        catch (Exception e) {
            e.printStackTrace();
            response.put("serialized_img", "null");
        }

        return response;
    }
}
