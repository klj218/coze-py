from enum import Enum, IntEnum
from typing import List, Optional

from cozepy.model import AsyncNumberPaged, CozeModel, NumberPaged, NumberPagedResponse
from cozepy.request import HTTPRequest, Requester
from cozepy.util import remove_url_trailing_slash


class BotPromptInfo(CozeModel):
    # Configured prompt of the bot.
    prompt: str


class BotOnboardingInfo(CozeModel):
    # Configured prologue of the bot.
    prologue: str = ""
    # The list of recommended questions configured for the bot.
    # This field will not be returned when user suggested questions are not enabled.
    suggested_questions: List[str] = []


class BotKnowledge(CozeModel):
    # Configured dataset ids of the bot.
    dataset_ids: List[str] = []
    # Whether to call knowledge base automatically.
    auto_call: bool = True
    # Configured search strategy of the bot, values: 0: semantic search, 1: hybrid search, 20: full-text search.
    search_strategy: int = 0


class BotModelInfo(CozeModel):
    # The ID of the model.
    model_id: str
    # The name of the model.
    model_name: str


class BotMode(IntEnum):
    SINGLE_AGENT = 0
    MULTI_AGENT = 1
    SINGLE_AGENT_WORKFLOW = 2


class BotPluginAPIInfo(CozeModel):
    # The ID of the tool.
    api_id: str
    # The name of the tool.
    name: str
    # The description of the tool.
    description: str


class BotPluginInfo(CozeModel):
    # The unique identifier for the plugin.
    plugin_id: str
    # The name of the plugin.
    name: str
    # The description of the plugin.
    description: str
    # The avatar URL for the plugin.
    icon_url: str
    # The list of tool information for the plugin. For more information, see PluginAPI object.
    api_info_list: List[BotPluginAPIInfo]


class SuggestReplyMode(str, Enum):
    # The bot does not suggest replies.
    DISABLE = "disable"
    # The bot suggests replies.
    ENABLE = "enable"
    # The bot suggests replies based on the customized prompt.
    CUSTOMIZED = "customized"


class BotSuggestReplyInfo(CozeModel):
    reply_mode: SuggestReplyMode
    customized_prompt: str = ""


class GradientPosition(CozeModel):
    left: Optional[float] = None
    right: Optional[float] = None


class CanvasPosition(CozeModel):
    width: Optional[float] = None
    height: Optional[float] = None
    left: Optional[float] = None
    top: Optional[float] = None


class BackgroundImageInfo(CozeModel):
    image_url: str = ""
    theme_color: Optional[str] = None
    gradient_position: Optional[GradientPosition] = None
    canvas_position: Optional[CanvasPosition] = None


class BotBackgroundImageInfo(CozeModel):
    web_background_image: Optional[BackgroundImageInfo] = None
    mobile_background_image: Optional[BackgroundImageInfo] = None


class VariableType(str, Enum):
    # The variable is a key-value pair.
    KVVariable = "KVVariable"
    # The variable is a list.
    ListVariable = "ListVariable"


class VariableChannel(str, Enum):
    # The variable is a custom variable.
    VariableChannelCustom = "custom"
    # The variable is a system variable.
    VariableChannelSystem = "system"
    # The variable is a location variable.
    VariableChannelLocation = "location"
    # The variable is a Feishu variable.
    VariableChannelFeishu = "feishu"
    # The variable is an app variable.
    VariableChannelAPP = "app"


class BotVariable(CozeModel):
    # The name of the variable.
    keyword: str
    # The default value of the variable.
    default_value: str
    # The type of the variable.
    variable_type: VariableType
    # The source of the variable.
    channel: VariableChannel
    # The description of the variable.
    description: str
    # Whether the variable is enabled.
    enable: bool
    # Whether the variable is supported in the prompt.
    prompt_enable: bool


class Bot(CozeModel):
    # The ID for the bot.
    bot_id: str
    # The name of the bot.
    name: Optional[str] = None
    # The description of the bot.
    description: Optional[str] = None
    # The URL address for the bot's avatar.
    icon_url: Optional[str] = None
    # The creation time, in the format of a 10-digit Unix timestamp in seconds (s).
    create_time: Optional[int] = None
    # The update time, in the format of a 10-digit Unix timestamp in seconds (s).
    update_time: Optional[int] = None
    # The latest version of the bot.
    version: Optional[str] = None
    # The prompt configuration for the bot. For more information, see Prompt object.
    prompt_info: Optional[BotPromptInfo] = None
    # The onboarding message configuration for the bot. For more information, see Onboarding object.
    onboarding_info: Optional[BotOnboardingInfo] = None
    # The knowledge configuration for the bot. For more information, see Knowledge object.
    knowledge: Optional[BotKnowledge] = None
    # The mode of the Bot, values: 0: Single Agent mode, 1: Multi Agent mode, 3: Single Agent Workflow mode.
    bot_mode: Optional[BotMode] = None
    # The plugins configured for the bot. For more information, see  Plugin object.
    plugin_info_list: Optional[List[BotPluginInfo]] = None
    # The model configured for the bot. For more information, see Model object.
    model_info: Optional[BotModelInfo] = None
    # The suggest reply info for the bot.
    suggest_reply_info: Optional[BotSuggestReplyInfo] = None
    # The background image info for the bot.
    background_image_info: Optional[BotBackgroundImageInfo] = None
    # The list of variables configured for the bot. For more information, see Variable object.
    variables: Optional[List[BotVariable]] = None


class SimpleBot(CozeModel):
    # The ID for the bot.
    bot_id: str
    # The name of the bot.
    bot_name: str
    # The description of the bot.
    description: str
    # The URL address for the bot's avatar.
    icon_url: str
    # The latest publish time of the bot, in the format of a 10-digit Unix timestamp in seconds (s).
    # This API returns the list of bots sorted in descending order by this field.
    publish_time: str


class UpdateBotResp(CozeModel):
    pass


class _PrivateListBotsData(CozeModel, NumberPagedResponse[SimpleBot]):
    space_bots: List[SimpleBot]
    total: int

    def get_total(self) -> Optional[int]:
        return self.total

    def get_has_more(self) -> Optional[bool]:
        return None

    def get_items(self) -> List[SimpleBot]:
        return self.space_bots


class BotsClient(object):
    """
    Bot class.
    """

    def __init__(self, base_url: str, requester: Requester):
        self._base_url = remove_url_trailing_slash(base_url)
        self._requester = requester

    def create(
        self,
        *,
        space_id: str,
        name: str,
        description: Optional[str] = None,
        icon_file_id: Optional[str] = None,
        prompt_info: Optional[BotPromptInfo] = None,
        onboarding_info: Optional[BotOnboardingInfo] = None,
        suggest_reply_info: Optional[BotSuggestReplyInfo] = None,
        **kwargs,
    ) -> Bot:
        url = f"{self._base_url}/v1/bot/create"
        body = {
            "space_id": space_id,
            "name": name,
            "description": description,
            "icon_file_id": icon_file_id,
            "prompt_info": prompt_info.model_dump() if prompt_info else None,
            "onboarding_info": onboarding_info.model_dump() if onboarding_info else None,
            "suggest_reply_info": suggest_reply_info.model_dump() if suggest_reply_info else None,
        }
        headers: Optional[dict] = kwargs.get("headers")

        return self._requester.request("post", url, False, Bot, body=body, headers=headers)

    def update(
        self,
        *,
        bot_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        icon_file_id: Optional[str] = None,
        prompt_info: Optional[BotPromptInfo] = None,
        onboarding_info: Optional[BotOnboardingInfo] = None,
        knowledge: Optional[BotKnowledge] = None,
        suggest_reply_info: Optional[BotSuggestReplyInfo] = None,
        **kwargs,
    ) -> UpdateBotResp:
        """
        Update the configuration of a bot.
        This API can be used to update all bots created through the Coze platform or via the API.
        In addition to updating the bot's name and description, avatar, personality and reply logic,
        and opening remarks, this API also supports binding a knowledge base to the bot.

        docs en: https://www.coze.com/docs/developer_guides/update_bot
        docs zh: https://www.coze.cn/docs/developer_guides/update_bot

        :param bot_id: The ID of the bot that the API interacts with.
        :param name: The name of the bot. It should be 1 to 20 characters long.
        :param description: The description of the Bot. It can be 0 to 500 characters long. The default is empty.
        :param icon_file_id: The file ID for the Bot's avatar. If no file ID is specified, the Coze platform will
        assign a default avatar for the bot. To use a custom avatar, first upload the local file through the Upload
        file interface and obtain the file ID from the interface response.
        :param prompt_info: The personality and reply logic of the bot.
        :param onboarding_info: The settings related to the bot's opening remarks.
        :param knowledge: The knowledge base that the bot uses to answer user queries.
        :param suggest_reply_info: The suggest reply info for the bot.
        :return: None
        """
        url = f"{self._base_url}/v1/bot/update"
        body = {
            "bot_id": bot_id,
            "name": name,
            "description": description,
            "icon_file_id": icon_file_id,
            "prompt_info": prompt_info.model_dump() if prompt_info else None,
            "onboarding_info": onboarding_info.model_dump() if onboarding_info else None,
            "knowledge": knowledge.model_dump() if knowledge else None,
            "suggest_reply_info": suggest_reply_info.model_dump() if suggest_reply_info else None,
        }
        headers: Optional[dict] = kwargs.get("headers")

        return self._requester.request(
            "post",
            url,
            False,
            cast=UpdateBotResp,
            body=body,
            headers=headers,
        )

    def publish(self, *, bot_id: str, connector_ids: Optional[List[str]] = None, **kwargs) -> Bot:
        url = f"{self._base_url}/v1/bot/publish"
        headers: Optional[dict] = kwargs.get("headers")
        if not connector_ids:
            connector_ids = ["1024"]
        body = {
            "bot_id": bot_id,
            "connector_ids": connector_ids,
        }

        return self._requester.request("post", url, False, Bot, headers=headers, body=body)

    def retrieve(self, *, bot_id: str, **kwargs) -> Bot:
        """
        Get the configuration information of the bot, which must have been published
        to the Bot as API channel.
        获取指定 Bot 的配置信息，此 Bot 必须已发布到 Bot as API 渠道中。

        docs en: https://www.coze.com/docs/developer_guides/get_metadata
        docs zh: https://www.coze.cn/docs/developer_guides/get_metadata

        :param bot_id: The ID of the bot that the API interacts with.
        要查看的 Bot ID。
        :return: bot object
        Bot 的配置信息
        """
        url = f"{self._base_url}/v1/bot/get_online_info"
        params = {"bot_id": bot_id}
        headers: Optional[dict] = kwargs.get("headers")

        return self._requester.request("get", url, False, Bot, params=params, headers=headers)

    def list(self, *, space_id: str, page_num: int = 1, page_size: int = 20) -> NumberPaged[SimpleBot]:
        """
        Get the bots published as API service.
        查看指定空间发布到 Bot as API 渠道的 Bot 列表。

        docs en: https://www.coze.com/docs/developer_guides/published_bots_list
        docs zh: https://www.coze.cn/docs/developer_guides/published_bots_list

        :param space_id: The ID of the space.
        Bot 所在的空间的 Space ID。Space ID 是空间的唯一标识。
        :param page_num: Pagination size. The default is 20, meaning that 20 data entries are returned per page.
        分页大小。默认为 20，即每页返回 20 条数据。
        :param page_size: Page number for paginated queries. The default is 1,
        meaning that the data return starts from the first page.
        分页查询时的页码。默认为 1，即从第一页数据开始返回。
        :return: Specify the list of Bots published to the Bot as an API channel in space.
        指定空间发布到 Bot as API 渠道的 Bot 列表。
        """
        url = f"{self._base_url}/v1/space/published_bots_list"

        def request_maker(i_page_num: int, i_page_size: int) -> HTTPRequest:
            return self._requester.make_request(
                "GET",
                url,
                params={
                    "space_id": space_id,
                    "page_size": i_page_size,
                    "page_index": i_page_num,
                },
                cast=_PrivateListBotsData,
                stream=False,
            )

        return NumberPaged(
            page_num=page_num,
            page_size=page_size,
            requestor=self._requester,
            request_maker=request_maker,
        )


class AsyncBotsClient(object):
    """
    Bot class.
    """

    def __init__(self, base_url: str, requester: Requester):
        self._base_url = remove_url_trailing_slash(base_url)
        self._requester = requester

    async def create(
        self,
        *,
        space_id: str,
        name: str,
        description: Optional[str] = None,
        icon_file_id: Optional[str] = None,
        prompt_info: Optional[BotPromptInfo] = None,
        onboarding_info: Optional[BotOnboardingInfo] = None,
        suggest_reply_info: Optional[BotSuggestReplyInfo] = None,
        **kwargs,
    ) -> Bot:
        url = f"{self._base_url}/v1/bot/create"
        body = {
            "space_id": space_id,
            "name": name,
            "description": description,
            "icon_file_id": icon_file_id,
            "prompt_info": prompt_info.model_dump() if prompt_info else None,
            "onboarding_info": onboarding_info.model_dump() if onboarding_info else None,
            "suggest_reply_info": suggest_reply_info.model_dump() if suggest_reply_info else None,
        }
        headers: Optional[dict] = kwargs.get("headers")

        return await self._requester.arequest("post", url, False, Bot, body=body, headers=headers)

    async def update(
        self,
        *,
        bot_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        icon_file_id: Optional[str] = None,
        prompt_info: Optional[BotPromptInfo] = None,
        onboarding_info: Optional[BotOnboardingInfo] = None,
        knowledge: Optional[BotKnowledge] = None,
        suggest_reply_info: Optional[BotSuggestReplyInfo] = None,
        **kwargs,
    ) -> UpdateBotResp:
        """
        Update the configuration of a bot.
        This API can be used to update all bots created through the Coze platform or via the API.
        In addition to updating the bot's name and description, avatar, personality and reply logic,
        and opening remarks, this API also supports binding a knowledge base to the bot.

        docs en: https://www.coze.com/docs/developer_guides/update_bot
        docs zh: https://www.coze.cn/docs/developer_guides/update_bot

        :param bot_id: The ID of the bot that the API interacts with.
        :param name: The name of the bot. It should be 1 to 20 characters long.
        :param description: The description of the Bot. It can be 0 to 500 characters long. The default is empty.
        :param icon_file_id: The file ID for the Bot's avatar. If no file ID is specified, the Coze platform will
        assign a default avatar for the bot. To use a custom avatar, first upload the local file through the Upload
        file interface and obtain the file ID from the interface response.
        :param prompt_info: The personality and reply logic of the bot.
        :param onboarding_info: The settings related to the bot's opening remarks.
        :param knowledge: The knowledge base that the bot uses to answer user queries.
        :param suggest_reply_info: The suggest reply info for the bot.
        :return: None
        """
        url = f"{self._base_url}/v1/bot/update"
        body = {
            "bot_id": bot_id,
            "name": name,
            "description": description,
            "icon_file_id": icon_file_id,
            "prompt_info": prompt_info.model_dump() if prompt_info else None,
            "onboarding_info": onboarding_info.model_dump() if onboarding_info else None,
            "knowledge": knowledge.model_dump() if knowledge else None,
            "suggest_reply_info": suggest_reply_info.model_dump() if suggest_reply_info else None,
        }
        headers: Optional[dict] = kwargs.get("headers")

        return await self._requester.arequest("post", url, False, cast=UpdateBotResp, body=body, headers=headers)

    async def publish(
        self,
        *,
        bot_id: str,
        connector_ids: Optional[List[str]] = None,
        **kwargs,
    ) -> Bot:
        url = f"{self._base_url}/v1/bot/publish"
        headers: Optional[dict] = kwargs.get("headers")
        if not connector_ids:
            connector_ids = ["1024"]
        body = {
            "bot_id": bot_id,
            "connector_ids": connector_ids,
        }

        return await self._requester.arequest("post", url, False, Bot, headers=headers, body=body)

    async def retrieve(self, *, bot_id: str) -> Bot:
        """
        Get the configuration information of the bot, which must have been published
        to the Bot as API channel.
        获取指定 Bot 的配置信息，此 Bot 必须已发布到 Bot as API 渠道中。

        docs en: https://www.coze.com/docs/developer_guides/get_metadata
        docs zh: https://www.coze.cn/docs/developer_guides/get_metadata

        :param bot_id: The ID of the bot that the API interacts with.
        要查看的 Bot ID。
        :return: bot object
        Bot 的配置信息
        """
        url = f"{self._base_url}/v1/bot/get_online_info"
        params = {"bot_id": bot_id}

        return await self._requester.arequest("get", url, False, Bot, params=params)

    async def list(self, *, space_id: str, page_num: int = 1, page_size: int = 20) -> AsyncNumberPaged[SimpleBot]:
        """
        Get the bots published as API service.
        查看指定空间发布到 Bot as API 渠道的 Bot 列表。

        docs en: https://www.coze.com/docs/developer_guides/published_bots_list
        docs zh: https://www.coze.cn/docs/developer_guides/published_bots_list

        :param space_id: The ID of the space.
        Bot 所在的空间的 Space ID。Space ID 是空间的唯一标识。
        :param page_num: Pagination size. The default is 20, meaning that 20 data entries are returned per page.
        分页大小。默认为 20，即每页返回 20 条数据。
        :param page_size: Page number for paginated queries. The default is 1,
        meaning that the data return starts from the first page.
        分页查询时的页码。默认为 1，即从第一页数据开始返回。
        :return: Specify the list of Bots published to the Bot as an API channel in space.
        指定空间发布到 Bot as API 渠道的 Bot 列表。
        """
        url = f"{self._base_url}/v1/space/published_bots_list"

        async def request_maker(i_page_num: int, i_page_size: int) -> HTTPRequest:
            return await self._requester.amake_request(
                "GET",
                url,
                params={
                    "space_id": space_id,
                    "page_size": i_page_size,
                    "page_index": i_page_num,
                },
                cast=_PrivateListBotsData,
                stream=False,
            )

        return await AsyncNumberPaged.build(
            page_num=page_num,
            page_size=page_size,
            requestor=self._requester,
            request_maker=request_maker,
        )
