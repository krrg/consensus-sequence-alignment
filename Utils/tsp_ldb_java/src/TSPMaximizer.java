import java.util.Map;

/**
 * Created by krr428 on 11/12/14.
 */
public class TSPMaximizer
{
    private IAdjacencyMatrix<Integer> matrix = null;

    public TSPMaximizer(IAdjacencyMatrix<Integer> adjacencyMatrix)
    {
        this.matrix = adjacencyMatrix;
    }

    private void invalidateCol(String col)
    {
        this.matrix.setColumn(col, Integer.MIN_VALUE);
    }

    private void invalidateRow(String row)
    {
        this.matrix.setRow(row, Integer.MIN_VALUE);
    }

    private String getNextAvailableRow()
    {
        final int LOWER_BOUND = 0;

        for (String row: matrix.getRows())
        {
            Map.Entry<String, Integer> maxEntry = matrix.getMaximumOnRow(row);
            if (maxEntry.getValue() > LOWER_BOUND)
            {
                System.out.println("Arbitrary node: " + maxEntry.getKey());
                return maxEntry.getKey();
            }
        }

        return null;
    }

    private void print_maximum_path()
    {
        String current = getNextAvailableRow();
        this.invalidateCol(current);

        while (true)
        {
            if (current == null || getNextAvailableRow() == null)
            {
                System.out.println();
                break;
            }

            Map.Entry<String, Integer> bestMatch = matrix.getMaximumOnRow(current);

            System.out.println("Bestmatch = " + bestMatch.getKey());

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
            else if (this.matrix.)

        }
    }

}
