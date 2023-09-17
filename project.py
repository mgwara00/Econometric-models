import numpy as np
import pandas as pd
import sys
import itertools

def main():
# Shows data in table
    sep()
    print(f"Hello, this tool helps with making econometrics models for one dependent variable using basic methods\n")
    table = create_table()
    table_str = table.to_string(index=False)
    print(f"This is your data table: \n{table_str}")
    sep()
# Shows coefficient of varitation
    cv_table = cv(table).to_string(dtype=False)
    print(f"Coefficient of variation for each column equals:\n{cv_table}\n")
    sep()
# Shows correlation table
    c_table = corr_table(table)
    print(f"Correlation table:\n{c_table}")
    sep()
# Shows Helwig's method
    print("The Helwig's method which counts integral informations capacity for each combination of explenatory variables.\nThis method helps with chosing the best combination of variables which explane the dependent variable")
    helwig_dict = helwig_method(c_table)
    helwig_table = pd.DataFrame(data=helwig_dict.values(), index=helwig_dict.keys(), columns =["HL"])
    pd.set_option('display.max_rows', 123)
    pd.set_option('display.max_columns', 10)
    print(helwig_table)
    max_value = helwig_table.max().to_string(dtype=False, index=False)
    max_index = helwig_table.idxmax().to_string(dtype=False, index=False)
    print(f"\nThe best combination is:{max_index} with hl= {max_value}")
    sep()

# Selection of parameters
    print("Proper parameters for the econometrics model where b is a parameter for residuals which balance econometrics model:\n")
    p = parameters(table, max_index)
    for value in p:
        print(f"{value}: {p[value]}")
    sep()

# Model veryfication
    model = f"{table.columns[0]} = "
    for value in p:
        model += f"{p[value]}*{value} + "

    model = model.rstrip(" + ")
    print(f"\nThe econometrics model: {model}")

    print(f"\nVector of residuals:")
    residuals = residual(table,p)
    print(residuals.to_string(dtype=False, index=False))
    sep()

    fi2 = veryfication(table,residuals)
    print(f"\nConvergence factor (Φ^2) equals: {fi2}")

    if  0 <+ fi2 <= 0.2:
        print("Econometrics model is well adapted")
    elif 0.2 < fi2 <= 0.4:
        print("Econometrics model is averagely adapted")
    elif fi2 > 0.4:
        print("Econometrics model is invalidly adapted")
    sep()

# Counts Φ2
def veryfication(table, residuals):
    y = table.loc[:,table.columns[0]]
    y = y.apply(lambda x: (x - y.mean())**2)
    ei = residuals.mul(residuals)
    fi2 = ei.sum() / y.sum()
    return fi2


# Counts vector of residuals
def residual(table, p):
    b = p.pop("b")
    e_lst = []
    for value in p:
        mult = table.loc[:,value].mul(p[value])
        e_lst.append(mult)

    df1 = pd.DataFrame(data=e_lst).T
    df1["b"] = b
    df1 = df1.sum(axis=1)
    estimators = table.loc[:,table.columns[0]].sub(df1)
    return estimators

# Counts parameters
def parameters(table, max_index):
    max_index = max_index.strip("()")
    max_index = max_index.split(", ")

    Y = table.loc[:,table.columns[0]]
    X = table.loc[:, max_index]
    lst = []
    for i in X.index:
        lst.append(1)
    X["b"] = lst
    result = (np.linalg.inv(X.T.dot(X))).dot(X.T.dot(Y))
    b_dict = {}
    for index,column in enumerate(X.columns):
        b_dict[column] = round(result[index], 3)

    return(b_dict)




# Counts helwigs method for table
def helwig_method(c_table):
    combinations = comb(c_table)
    vector_r = c_table.loc[c_table.index[0]]
    helwig_dict = {}

    for i in combinations:
        if not isinstance(i, tuple):
            hl = vector_r.at[i] ** 2
            helwig_dict[i] = hl
        else:
            hl = 0
            for r in i:
                hl += vector_r.at[r]**2 / (1+corr_sum(r, i, c_table))
            helwig_dict[i] = hl
    return helwig_dict

# Counts denominator in dil method
def corr_sum(r, combination, c_table):
    result = 0
    for tupla in itertools.combinations(combination, 2):
        if r in tupla:
            result += abs(c_table.at[tupla[0],tupla[1]])
        else:
            pass
    return result

# Creates list of combinations
def comb(corr_t):
    exp_variable_list = []
    combinations = []
    for  column in corr_t.columns:
        exp_variable_list.append(column)
    exp_variable_list.pop(0)
    for variable in exp_variable_list:
        combinations.append(variable)

    for combination in gen_combs(exp_variable_list):
        combinations.append(combination)
    return combinations


# Generates combinations depended at number of variables
def gen_combs(list):
    for r in range(2, len(list)+1):
        combs = itertools.combinations(list, r)
        for comb in combs:
            yield comb

# Creates correlation table
def corr_table(t):
    correlations = np.corrcoef(t, rowvar=False)
    correlations_table = pd.DataFrame(np.triu(correlations), columns=t.columns, index=t.columns)
    return correlations_table

# Collects data from user and creats a table
def create_table(csv_file = None):
    if csv_file is None:
        csv_file = sys.argv[1]
    try:
        data = pd.read_csv(csv_file)
        df = pd.DataFrame(data)
        return df
    except FileNotFoundError:
        sys.exit("CSV file doesn't exist")
    except pd.errors.ParserError:
        sys.exit("Incorrect type of the file")

# Counts coefficient of variation for table
def cv(t):
    _cv = lambda x: f"{np.std(x)/np.mean(x) * 100:.3f}%"
    return t.apply(_cv)

def sep():
    print("______________________________________________________________________________________________________________________________")

if __name__ == "__main__":
    main()
