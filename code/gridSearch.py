from sklearn.model_selection import ParameterGrid

class gridSearch:

    def __init__(self, build_fn, param_grid, vocab_size, sentence_size):
        self.build_fn = build_fn
        self.param_grid = param_grid
        self.best_score = 0
        self.best_params = None
        self.results = []
        self.vocab_size = vocab_size
        self.sentence_size = sentence_size

    def fit(self, X, y, X_test, y_test, callbacks):

        for g in ParameterGrid(self.param_grid):
            model = self.build_fn(vocab_size=self.vocab_size, sentence_size=self.sentence_size, mergeMode=g['mergeMode'])

            print('\nUsing parameters:', g)
            model.fit(X, y, batch_size=g['batch_size'], epochs=g['epochs'], shuffle=True, callbacks=callbacks)

            print('Evaluating')
            loss, acc = model.evaluate(X_test, y_test, verbose=1)
            print('Loss: %f - Accuracy: %f' % (loss, acc))

            self.results.append({'loss':loss, 'acc':acc, 'params':g})

            if acc > self.best_score:
                self.best_score = acc
                self.best_params = g

                # Save model
                print("Saving model")
                model.save("../resources/model.h5")
                # model_json = model.to_json()
                # with open("../resources/model.json", "w") as json_file:
                #     json_file.write(model_json)
                #
                # # serialize weights to HDF5
                # model.save_weights("../resources/weights.h5")

    def summary(self):
        # Summarize results
        print('\nSummary')
        print("Best: %f using %s" % (self.best_score, self.best_params))
        for res in self.results:
            print("Loss: %f\t%f\twith: %r" % (res['loss'], res['acc'], res['params']))