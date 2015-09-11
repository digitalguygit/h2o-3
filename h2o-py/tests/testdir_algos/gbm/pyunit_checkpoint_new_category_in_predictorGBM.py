import sys
sys.path.insert(1,"../../../")
import h2o, tests

def checkpoint_new_category_in_predictor():

    sv1 = h2o.upload_file(h2o.locate("smalldata/iris/setosa_versicolor.csv"))
    sv2 = h2o.upload_file(h2o.locate("smalldata/iris/setosa_versicolor.csv"))
    vir = h2o.upload_file(h2o.locate("smalldata/iris/virginica.csv"))

    m1 = h2o.gbm(x=sv1[[0,1,2,4]], y=sv1[3], ntrees=100)

    m2 = h2o.gbm(x=sv2[[0,1,2,4]], y=sv2[3], ntrees=200, checkpoint=m1.id)

    # attempt to continue building model, but with an expanded categorical predictor domain.
    # this should fail until we figure out proper behavior
    try:
        m3 = h2o.gbm(x=vir[[0,1,2,4]], y=vir[3], ntrees=200, checkpoint=m1.id)
        assert False, "Expected continued model-building to fail with new categories introduced in predictor"
    except EnvironmentError:
        pass

    # attempt to predict on new model, but with observations that have expanded categorical predictor domain.
    predictions = m2.predict(vir)

if __name__ == '__main__':
    tests.run_test(sys.argv, checkpoint_new_category_in_predictor)