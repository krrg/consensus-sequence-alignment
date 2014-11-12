import java.util.Collection;
import java.util.List;
import java.util.Map;

/**
 * Created by krr428 on 11/12/14.
 */
public interface IAdjacencyMatrix<T extends Comparable<T>>
{
    public void add(String row, String col, T value);

    public boolean has(String row, String col);

    public T get(String row, String col);

    public int getNumberRows();

    public void setColumn(String col, T value);

    public void setRow(String row, T value);

    public void setRow(String row, List<T> values);

    public Map.Entry<String, T> getMaximumOnRow(String row);

    public List<String> getRows();

}
