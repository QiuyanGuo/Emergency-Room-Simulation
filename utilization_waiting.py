from scipy.stats import truncnorm


def time_spend(mean,sd,min,max,num):
    generator = truncnorm((min-mean)/sd, (max-mean)/sd, loc=mean, scale=sd)
    time = generator.rvs(num)
    return time


def sum_truncnorm(mean,sd,min,max,num):
    generator = truncnorm((min-mean)/sd, (max-mean)/sd, loc=mean, scale=sd)
    time = generator.rvs(num)
    return sum(time)


def rate(time, target):
    return time/(target*60)

