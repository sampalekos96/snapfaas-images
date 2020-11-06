package srv;

import com.drew.imaging.ImageMetadataReader;
import com.drew.metadata.Directory;
import com.drew.metadata.Metadata;
import com.drew.metadata.Tag;
import org.json.simple.JSONObject;

import java.io.File;
import java.util.Base64;

public class workload {

    public workload() {

    }

    public JSONObject handle(JSONObject req) {

        JSONObject response = new JSONObject();

        try {
            Metadata metadata = ImageMetadataReader.readMetadata(new File("/srv/"+req.get("img")));

            StringBuilder sb = new StringBuilder();
            for (Directory directory : metadata.getDirectories()) {
                for (Tag tag : directory.getTags()) {
                    sb.append(String.format("[%s] - %s = %s\n",
                            directory.getName(), tag.getTagName(), tag.getDescription()));
                }
                if (directory.hasErrors()) {
                    for (String error : directory.getErrors()) {
                        sb.append(String.format("ERROR: %s", error));
                    }
                }
            }

            String metaString = Base64.getEncoder().encodeToString(sb.toString().getBytes());
            response.put("metadata", metaString);
        }
        catch (Exception e) {
            System.out.println(e.getCause());
            response.put("metadata", "null");
        }

        return response;
    }
}
