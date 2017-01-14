import services


Meiju = services.MeiJu()


def search(page, **kwargs):
    c_list = Meiju.search(page, PAGE_ROWS, **kwargs)
    for one in c_list["data"]["results"]:
        item = ListItem(**{
            'label': one.get("title"),
            'path': plugin.url_for("detail", seasonId=one.get("id")),
            'icon': one["cover"],
            'thumbnail': one["cover"],
        })
        item.set_info("video", {"plot": one.get("brief", ""),
                                "rating ": float(one["score"]),
                                "genre": one["cat"],
                                "season": one["seasonNo"]})
        item._listitem.setArt({"poster": one["cover"]})
        item.set_is_playable(False)
        yield item


def get_album(albumId):
    c_list = Meiju.get_album(albumId)
    for one in c_list["data"]["results"]:
        item = ListItem(**{
            'label': one.get("title"),
            'path': plugin.url_for("detail", seasonId=one.get("id")),
            'icon': one["cover"],
            'thumbnail': one["cover"],
        })
        item.set_info("video", {"plot": one.get("brief", ""),
                                "rating ": float(one["score"]),
                                "genre": one["cat"],
                                "season": one["seasonNo"]})
        item._listitem.setArt({"poster": one["cover"]})
        item.set_is_playable(False)
        yield item
