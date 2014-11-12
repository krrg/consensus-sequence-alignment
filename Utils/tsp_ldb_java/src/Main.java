/**
 * Created by krr428 on 11/12/14.
 */
import org.iq80.leveldb.*;
import static org.fusesource.leveldbjni.JniDBFactory.*;
import java.io.*;

public class Main
{
    public static void main(String [] args)
    {
//        String frows = "/home/krr428/NetBeansProjects/consensus-sequence-alignment/Fasta/reads/synthetic.noerror.large.fasta.txt";
//        String fmatrix = "/home/krr428/NetBeansProjects/consensus-sequence-alignment/Fasta/matrix/synthetic.noerror.large.matrix";

        if (args.length < 2)
        {
            System.out.println("Usage: java -jar tsp_ldb_java.jar [READS FILE] [MATRIX FILE] > [OUTPUT_FILE]");
            System.exit(1);
        }

        String frows = args[0];
        String fmatrix = args[1];

        LevelAdjacencyMatrix matrix = LevelAdjacencyMatrix.createAdjacencyTable(frows, fmatrix);


        TSPMaximizer maximizer = new TSPMaximizer(matrix);
        maximizer.print_maximum_path();
    }

}
