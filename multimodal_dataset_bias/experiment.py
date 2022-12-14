import os
import pytorch_lightning as pl
from argparse import ArgumentParser
from utils.file import save_file
from utils.nn_utils import make_trainer
from data import make_data
from model import Model

def main(config):
    seed = config.__dict__.pop("seed")
    save_file(config, os.path.join(config.dpath, "args.pkl"))
    os.makedirs(config.dpath, exist_ok=True)
    pl.seed_everything(seed)
    data_train, data_val, data_test = make_data(seed, config.n_examples, config.train_ratio, config.data_dim,
        config.batch_size, config.n_workers)
    model = Model(seed, config.dpath, config.task, config.data_dim, config.hidden_dims, config.latent_dim, config.lr,
        config.n_samples, config.n_posteriors, config.checkpoint_fpath, config.posterior_params_fpath)
    trainer = make_trainer(config.dpath, seed, config.n_epochs, config.patience)
    if config.is_test:
        trainer.test(model, data_test)
    else:
        trainer.fit(model, data_train, data_val)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--task", type=str, required=True)
    parser.add_argument("--dpath", type=str, default="results")
    parser.add_argument("--checkpoint_fpath", type=str, default=None)
    parser.add_argument("--posterior_params_fpath", type=str, default=None)
    parser.add_argument("--n_examples", nargs="+", type=int, default=[1000, 1000])
    parser.add_argument("--train_ratio", type=float, default=0.8)
    parser.add_argument("--data_dim", type=int, default=1)
    parser.add_argument("--hidden_dims", nargs="+", type=int, default=[20, 20])
    parser.add_argument("--latent_dim", type=int, default=10)
    parser.add_argument("--n_samples", type=int, default=500)
    parser.add_argument("--n_posteriors", type=int, default=500)
    parser.add_argument("--lr", type=float, default=0.01)
    parser.add_argument("--n_epochs", type=int, default=-1)
    parser.add_argument("--patience", type=int, default=20)
    parser.add_argument("--batch_size", type=int, default=50)
    parser.add_argument("--n_workers", type=int, default=20)
    parser.add_argument("--is_test", action="store_true")
    main(parser.parse_args())