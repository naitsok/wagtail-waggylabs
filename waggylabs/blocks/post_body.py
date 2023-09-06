from waggylabs.blocks.base_body import BaseBodyBlock
from waggylabs.blocks.post_meta import PostMetaBlock
from waggylabs.blocks.post_series import PostSeriesBlock


class PostBodyBlock(BaseBodyBlock):
    """Post body block has specific additional blocks."""
    post_meta = PostMetaBlock()
    post_series = PostSeriesBlock()
    
    class Meta:
        block_counts = {
            'post_meta': { 'max_num': 1 },
            'page_info': { 'max_num': 1 },
        }