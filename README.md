   # Econometrics model
    #### Description:
    Hello, as my project i created an app which helps the user create econometrics model from a data table given as a ".csv" file (It's required when you run the program to give another argument which is name of the csv file which contain your data table). In the data table columns should represent variables where the first column represents dependent variable and other columns represent explanatory variables.

    First of all the program represents the imported data table and counts coefficients of variation for each column, then the program makes correlation matrix for all variables which is required to make all next calculations. In the next step, the program checks all possible combinations of explanatory variables and counts "integral information capacity" for each combination which is necessary to choose the best combination. In short this method looks for combinations where explanatory variables are strongly correlated with dependent variable and weakly correlated with each other.

    In the next step the program counts parameters for each explanatory variable which will make the econometrics model more adapted.

    Lastly, the program shows the chosen econometrics model and counts convergence factor for our model. Convergence factor explains how well the econometrics model explains the dependent variable. Additionally the program interpret convergence factor for us using requirements presented below:

    Convergence factor in range  (0 - 0.2) - Econometrics model is well adapted
    Convergence factor in range  (0.21 - 0.4) - Econometrics model is averagely adapted
    Convergence factor in range  (0.41 - 1) - Econometrics model is invalidly adapted
