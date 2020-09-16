package bin;

import java.io.*;

public class setup_java {

    public static void main(String[] argv) {

        /* for language snapshot */
        int cores = Runtime.getRuntime().availableProcessors();
        try {
            Process[] proc_list = new Process[cores];
            for (int i=1; i<cores; i++) {
                proc_list[i] = Runtime.getRuntime().exec(String.format("taskset -c %d outl 124 0x3f0", i));
            }
            proc_list[0] = Runtime.getRuntime().exec("taskset -c 0 outl 124 0x3f0");
            int exitVal = proc_list[0].waitFor();
            assert  exitVal == 0: "Err in enabling language snapshot";
        }
        catch (Exception e) {
            System.out.println(e);
            System.exit(1);
        }

        try {
            /* mount appfs */
            Process process = Runtime.getRuntime().exec("mount -r /dev/vdb /srv");
            int exitVal = process.waitFor();
            assert  exitVal == 0: "Err in mounting appfs";

            /* get appfs srv packages */
//            File pkg_names = new File("/srv/package");
//            String cp_path = "";
//            for (String pkg: pkg_names.list()) {
//                cp_path += ":/srv/package/"+pkg;
//            }
//            System.out.println("cp path: "+cp_path);

//            process = Runtime.getRuntime().exec("umount /srv");
//            exitVal = process.waitFor();
//            assert  exitVal == 0: "Err in mounting appfs";

//            String cmd = String.format("java -cp \".:/bin/*%s\" -Djava.library.path=/bin bin.runtime_workload", cp_path);

            /* executing the actual runtime workload */
//            Runtime.getRuntime().exec(new String[] {"java", "-cp", ".:/bin/*"+cp_path, "-Djava.library.path=/bin", "bin.runtime_workload"});

//            StringBuilder output = new StringBuilder();
//            BufferedReader reader = new BufferedReader(
//                    new InputStreamReader(process.getErrorStream()));
//            String line;
//            while ((line = reader.readLine()) != null) {
//                output.append(line + "\n");
//            }
//            System.out.println(output);
//            System.out.println(cmd);
        }
        catch (Exception e) {
            System.out.println(e);
            System.exit(1);
        }
    }
}
