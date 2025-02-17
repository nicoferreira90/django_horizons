from wagtail import blocks


class RichTextBlock(blocks.RichTextBlock):

    class Meta:
        template = "blog/rich_text_block.html"
        icon = "edit"
        label = "Full RichText"
