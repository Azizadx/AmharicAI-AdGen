from tokenizers import Tokenizer, models, normalizers, pre_tokenizers, trainers, processors, decoders
from transformers import PreTrainedTokenizerFast

class CustomTokenizer:
    def __init__(self, vocab_size=20_000, min_frequency=2):
        self.tokenizer = Tokenizer(models.WordPiece(unk_token='[UNK]'))
        self.tokenizer.normalizer = normalizers.Sequence([normalizers.Lowercase(), normalizers.NFKD()])
        self.tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
        self.trainer = trainers.WordPieceTrainer(
            vocab_size=vocab_size,
            special_tokens=['[UNK]', '[PAD]', '[CLS]', '[SEP]', '[MASK]'],
            min_frequency=min_frequency,
            continuing_subword_prefix=''
        )
        self.processor = processors.TemplateProcessing(
            single=f'[CLS]:0 $A:0 [SEP]:0',
            pair=f'[CLS]:0 $A:0 [SEP]:0 $B:1 [SEP]:1',
            special_tokens=[
                ('[CLS]', self.tokenizer.token_to_id('[CLS]')),
                ('[SEP]', self.tokenizer.token_to_id('[SEP]'))
            ]
        )
        self.decoder = decoders.WordPiece(prefix='##')
        self.transformers_tokenizer = None

    def train_tokenizer(self, input_files):
        self.tokenizer.train(input_files, trainer=self.trainer)

    def train_tokenizer_iterable(self, iterable_data):
        self.tokenizer.train_from_iterator(iterable_data, trainer=self.trainer)

    def setup_post_processing(self):
        cls_id = self.tokenizer.token_to_id('[CLS]')
        sep_id = self.tokenizer.token_to_id('[SEP]')
        self.tokenizer.post_processor = processors.TemplateProcessing(
            single=f'[CLS]:0 $A:0 [SEP]:0',
            pair=f'[CLS]:0 $A:0 [SEP]:0 $B:1 [SEP]:1',
            special_tokens=[
                ('[CLS]', cls_id),
                ('[SEP]', sep_id)
            ]
        )

    def setup_transformers_tokenizer(self):
        self.transformers_tokenizer = PreTrainedTokenizerFast(
            tokenizer_object=self.tokenizer,
            unk_token='[UNK]',
            pad_token='[PAD]',
            cls_token='[CLS]',
            sep_token='[SEP]',
            mask_token='[MASK]'
        )

    def save_transformers_tokenizer(self, save_path):
        if self.transformers_tokenizer:
            self.transformers_tokenizer.save_pretrained(save_path)
        else:
            raise ValueError("Transformers tokenizer not set. Run setup_transformers_tokenizer first.")
