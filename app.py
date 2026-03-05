from flask import Flask, render_template, request
import numpy as np
from scipy.stats import t
from statistics import stdev
from scipy import stats

app = Flask(__name__)

def two_sample(a, b, alternative):

    xbar1 = np.mean(a)
    xbar2 = np.mean(b)

    sd1 = stdev(a)
    sd2 = stdev(b)

    n1 = len(a)
    n2 = len(b)

    alpha = 0.05/2
    df = n1+n2-2

    se = np.sqrt((sd1**2)/(n1) + (sd2**2)/n2)

    t_table_pos = t.ppf(1-alpha, df)
    t_table_neg = t.ppf(alpha, df)

    tcal = ((xbar1-xbar2)-0)/se

    if alternative == "two-sided":
        pvalue = 2*(1-t.cdf(abs(tcal), df))
    elif alternative == "left":
        pvalue = t.cdf(tcal, df)
    else:
        pvalue = 1-t.cdf(tcal, df)

    scipy_result = stats.ttest_ind(a, b, alternative='two-sided', equal_var=False)

    return {
        "tcal": round(tcal,4),
        "pvalue": round(pvalue,6),
        "t_table_pos": round(t_table_pos,4),
        "t_table_neg": round(t_table_neg,4),
        "scipy": str(scipy_result)
    }


@app.route("/", methods=["GET","POST"])
def index():

    result = None

    if request.method == "POST":

        sample1 = request.form["sample1"]
        sample2 = request.form["sample2"]
        alternative = request.form["alt"]

        a = list(map(float, sample1.split(",")))
        b = list(map(float, sample2.split(",")))

        result = two_sample(a,b,alternative)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)