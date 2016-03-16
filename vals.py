import pickle

Npts = 1

for i in range(Npts):
    try:
        with open('rf0.pickle', 'rb') as f:
            size, rfc,test = pickle.load(f)

        with open('rfsmall0.pickle', 'wb') as f:
            pickle.dump([size, rfc.grid_scores_, test], f)
    except:
	    pass
