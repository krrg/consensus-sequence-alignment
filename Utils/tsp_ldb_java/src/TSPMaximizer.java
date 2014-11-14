import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/**
 * Created by krr428 on 11/12/14.
 */
public class TSPMaximizer
{
    private IAdjacencyMatrix<Integer> matrix = null;
    private Set<String> deletedRows = null;

    public TSPMaximizer(IAdjacencyMatrix<Integer> adjacencyMatrix)
    {
        this.matrix = adjacencyMatrix;
        this.deletedRows = new HashSet<>();
    }

    private void invalidateCol(String col)
    {
        this.matrix.setColumn(col, Integer.MIN_VALUE);
    }

    private void invalidateRow(String row)
    {
        deletedRows.add(row);
//        this.matrix.setRow(row, Integer.MIN_VALUE);
    }

    private String getNextAvailableRow()
    {
        final int LOWER_BOUND = 0;

        for (String row: matrix.getRows())
        {
            if (deletedRows.contains(row))
            {
                continue;
            }

            Map.Entry<String, Integer> maxEntry = matrix.getMaximumOnRow(row);
            if (maxEntry.getValue() > LOWER_BOUND)
            {
                return maxEntry.getKey();
            }
        }

        return null;
    }

    public void print_maximum_path()
    {
        String current = getNextAvailableRow();
        this.invalidateCol(current);

        while (true)
        {
            if (current == null || this.deletedRows.size() == this.matrix.getNumberRows())
            {
                System.out.println();
                break;
            }

            Map.Entry<String, Integer> bestMatch = matrix.getMaximumOnRow(current);

            if (bestMatch.getValue() <= 0)
            {
                System.out.println();
                this.invalidateRow(current);
                current = this.getNextAvailableRow();
                if (current != null)
                {
                    System.out.println(current);
                }
                this.invalidateCol(current);
                continue;
            }
            else if (this.matrix.getMaximumOnRow(bestMatch.getKey()).getValue() <= 0)
            {
                System.out.println();
                this.invalidateRow(current);
                current = this.getNextAvailableRow();
                continue;
            }

            this.invalidateCol(bestMatch.getKey());
            this.invalidateRow(current);

            this.matrix.put(bestMatch.getKey(), current, Integer.MIN_VALUE);
            System.out.println(bestMatch.getKey());
            current = bestMatch.getKey();
        }
    }

}
