import org.iq80.leveldb.*;
import static org.fusesource.leveldbjni.JniDBFactory.*;
import java.io.*;
import java.util.*;

/**
 * Created by krr428 on 11/12/14.
 */
public class LevelAdjacencyMatrix implements IAdjacencyMatrix<Integer>
{
    private DB db = null;
    private List<String> rows = null;

    public static LevelAdjacencyMatrix createAdjacencyTable(String frows, String fmatrix)
    {
        try
        {
            LevelAdjacencyMatrix matrix = new LevelAdjacencyMatrix(readRows(frows));

            try (Scanner sc = new Scanner(new BufferedInputStream(new FileInputStream(fmatrix))))
            {
                int i = 0;
                while (sc.hasNextLine())
                {
                    String row = matrix.rows.get(i);
                    List<Integer> rowInts = new ArrayList<>();
                    Scanner lineScan = new Scanner(sc.nextLine());
                    while (lineScan.hasNextInt())
                    {
                        rowInts.add(lineScan.nextInt());
                    }
                    matrix.setRow(row, rowInts);
                    i++;
                }
            }

            return matrix;
        }
        catch (IOException e)
        {
            System.out.println("Could not open input files!");

            return null;
        }

    }

    private static List<String> readRows(String filename) throws IOException
    {
        try (Scanner sc = new Scanner(new BufferedInputStream(new FileInputStream(filename))))
        {
            List<String> rows = new ArrayList<>();

            while (sc.hasNextLine())
            {
                rows.add(sc.nextLine());
            }

            return rows;
        }
    }


    public LevelAdjacencyMatrix(List<String> rows)
    {
        this.rows = rows;
        try
        {
            __createDatabase();
        }
        catch (IOException ex)
        {
            System.out.println("Error, could not open database.");
            System.out.println(ex);
        }
    }

    private void __createDatabase() throws IOException
    {
        Options options = new Options();
        options.createIfMissing(true);
        this.db = factory.open(new File("/tmp/" + String.valueOf(System.currentTimeMillis())), options);
    }

    @Override
    public void add(String row, String col, Integer value)
    {
        db.put(bytes(row + col), bytes(value.toString()));
    }

    @Override
    public boolean has(String row, String col)
    {
        return db.get(getDualKey(row, col)) != null;
    }

    @Override
    public Integer get(String row, String col)
    {
        return Integer.parseInt(asString(db.get(getDualKey(row, col))));
    }

    @Override
    public int getNumberRows()
    {
        return rows.size();
    }

    @Override
    public void setColumn(String col, Integer value)
    {
        try (WriteBatch batch = db.createWriteBatch())
        {
            for (String row : rows)
            {
                batch.put(getDualKey(row, col), bytes(value.toString()));
            }
            db.write(batch);
        }
        catch (IOException e)
        {
            System.out.println("Warning: Could not close batch on setCol");
        }
    }

    @Override
    public void setRow(String row, Integer value)
    {
        this.setRow(row, Collections.nCopies(rows.size(), value));
    }

    private byte[] getDualKey(String row, String col)
    {
        return bytes(row + col);
    }

    @Override
    public void setRow(String row, List<Integer> values)
    {
        try (WriteBatch batch = db.createWriteBatch())
        {
            for (int i = 0; i < values.size() && i < rows.size(); i++)
            {
                batch.put(getDualKey(row, rows.get(i)), bytes(values.get(i).toString()));
            }
            db.write(batch);
        }
        catch (IOException ex)
        {
            System.out.println("Warning: Could not close batch on setRow");
        }

    }

    @Override
    public Map.Entry<String, Integer> getMaximumOnRow(String row)
    {
        DBIterator iter = db.iterator();
        iter.seek(bytes(row));

        int maxVal = Integer.MIN_VALUE;
        String maxCol = null;

        for (String col : rows)
        {
            int i = this.get(row, col);
            if (i > maxVal)
            {
                maxVal = i;
                maxCol = col;
            }
        }

        return new AbstractMap.SimpleImmutableEntry<String, Integer>(maxCol, maxVal);
    }

    @Override
    public List<String> getRows()
    {
        return Collections.unmodifiableList(this.rows);
    }
}
