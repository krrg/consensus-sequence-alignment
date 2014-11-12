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
        String frows = "/home/krr428/NetBeansProjects/consensus-sequence-alignment/Fasta/reads/synthetic.noerror.small.fasta.txt";
        String fmatrix = "/home/krr428/NetBeansProjects/consensus-sequence-alignment/Fasta/matrix/synthetic.noerror.small.matrix";

        LevelAdjacencyMatrix matrix = LevelAdjacencyMatrix.createAdjacencyTable(frows, fmatrix);

        System.out.println(matrix.getNumberRows());
    }

}
