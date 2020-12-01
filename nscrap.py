import requests as r
from bs4 import BeautifulSoup as bs
import urllib
import json
import time
import unicodedata

class clarin():
    def __init__(self):
        self.url='https://www.clarin.com'
    
    
    urlc='https://login.clarin.com/comments.getComments'
    urlcp='https://login.clarin.com/comments.getComments?categoryID=Com_03&streamID=H1Y2WMTS-&includeSettings=true&threaded=true&includeStreamInfo=true&includeUserOptions=true&includeUserHighlighting=true&lang=es&ctag=comments_v2&APIKey=2_fq_ZOJSR4xNZtv2rA8DALl1Gxp7yTYMb3UdER6zerupB55mwkzh9pVBz4Blzi8SW&source=showCommentsUI&sourceData=%7B%22categoryID%22%3A%22Com_03%22%2C%22streamID%22%3A%22H1Y2WMTS-%22%7D&sdk=js_latest&authMode=cookie&pageURL=https%3A%2F%2Fwww.clarin.com%2Fpolitica%2Facuerdo-cambiemos-massismo-echar-vido-camara-diputados_0_H1Y2WMTS-.html&format=jsonp&callback=gigya.callback&context=R4169081209'
    urlp=urllib.parse.urlparse(urlcp)
    keys=urllib.parse.parse_qs(urlp.query)
 
    
    def get(self,url):

        nota=r.get(url)
        sopa=bs(nota.content,features="lxml")
        ps=sopa.find('div','body-nota').findAll('p')
        st=sopa.find('div','body-nota').findAll('strong')
        self.volanta=sopa.find('p','volanta').text
        self.titulo=sopa.find('h1').text
        self.bajada=sopa.find('div','bajada').find('h2').text
        texto=list()
        for p in ps:
            if p.text == "COMENTARIOS":
                break
            texto.append(p.text)
        bolds=list()    
        for b in st:
            bolds.append(b.text)            
        self.cuerpo=' '.join(texto)
        self.bold=' '.join(bolds)
        self.bolds=bolds
        keys=self.keys
        keys['pageURL'][0]=url
        keys['streamID'][0]=url[-14:-5]
        cm=r.get(self.urlc,params=keys)
        d = json.loads(cm.text[15:-2])
        self.comm=[x['commentText'] for x in d['comments']]
        self.com=' '.join(self.comm)
      
    def hoy(self):            
        notas=r.get(self.url)
        sopa=bs(notas.content,features="lxml")
        urls=[x.find('a').get('href') for x in sopa.find_all('article')]
        boxs=list()

        for x in sopa.find_all('div', {'class':'on-demand'}):
            boxs.append(self.url+x.get('data-src'))

        reqs=list()
        # son 69 pero hasta el 8 tienen cosas
        for x in boxs[:9]:
            reqs.append(r.get(x))
            #para evitar ban pongo pausa
            time.sleep(0.2)

        box0=json.loads(reqs[0].content.decode().strip('()'))['data']
        sopa0=bs(box0,features="lxml")

        for x in sopa0.find_all('a'): 
            urls.append(x.get('href'))


        for n,x in enumerate(reqs[1:]):
            box=json.loads(x.content.decode().strip('()'))['data']
            sopa=bs(box,features="lxml")
            for y in sopa.find_all('article'):      
                urls.append(y.find('a').get('href'))                                        

        box7=json.loads(reqs[7].content.decode().strip('()'))['data']
        sopa7=bs(box7,features="lxml")
        for x in sopa7.find('div',{'class':'mas-vistas'}).find_all('div')[1].find_all('div',{'onclick' : True}):
            urls.append(x.get('onclick')[13:-11])  
        urls2=list()    
        for u in urls:
            if u[:4] == 'http':
                urls2.append(u)
            else:
                urls2.append('https://www.clarin.com'+u)
        self.urls=urls2   
        
class p12():
    
    def __init__(self,url):
        self.url=url
    #poner a mano el limite de comentarios, por default en la pagina=10
    x=r'{"query":"query CoralEmbedStream_Embed($assetId: ID, $assetUrl: String, $commentId: ID!, $hasComment: Boolean!, $excludeIgnored: Boolean, $sortBy: SORT_COMMENTS_BY!, $sortOrder: SORT_ORDER!) {\n  me {\n    id\n    state {\n      status {\n        username {\n          status\n          __typename\n        }\n        banned {\n          status\n          __typename\n        }\n        alwaysPremod {\n          status\n          __typename\n        }\n        suspension {\n          until\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  asset(id: $assetId, url: $assetUrl) {\n    ...CoralEmbedStream_Configure_asset\n    ...CoralEmbedStream_Stream_asset\n    ...CoralEmbedStream_AutomaticAssetClosure_asset\n    __typename\n  }\n  ...CoralEmbedStream_Stream_root\n  ...CoralEmbedStream_Configure_root\n}\n\nfragment CoralEmbedStream_Stream_root on RootQuery {\n  me {\n    state {\n      status {\n        username {\n          status\n          __typename\n        }\n        banned {\n          status\n          __typename\n        }\n        alwaysPremod {\n          status\n          __typename\n        }\n        suspension {\n          until\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    ignoredUsers {\n      id\n      __typename\n    }\n    role\n    __typename\n  }\n  settings {\n    organizationName\n    __typename\n  }\n  ...TalkSlot_StreamTabPanes_root\n  ...TalkSlot_StreamFilter_root\n  ...CoralEmbedStream_Comment_root\n  __typename\n}\n\nfragment CoralEmbedStream_Comment_root on RootQuery {\n  me {\n    ignoredUsers {\n      id\n      __typename\n    }\n    __typename\n  }\n  ...TalkSlot_CommentInfoBar_root\n  ...TalkSlot_CommentAuthorName_root\n  ...TalkEmbedStream_DraftArea_root\n  ...TalkEmbedStream_DraftArea_root\n  __typename\n}\n\nfragment TalkEmbedStream_DraftArea_root on RootQuery {\n  __typename\n}\n\nfragment CoralEmbedStream_Stream_asset on Asset {\n  comment(id: $commentId) @include(if: $hasComment) {\n    ...CoralEmbedStream_Stream_comment\n    parent {\n      ...CoralEmbedStream_Stream_singleComment\n      parent {\n        ...CoralEmbedStream_Stream_singleComment\n        parent {\n          ...CoralEmbedStream_Stream_singleComment\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  id\n  title\n  url\n  isClosed\n  created_at\n  settings {\n    moderation\n    infoBoxEnable\n    infoBoxContent\n    premodLinksEnable\n    questionBoxEnable\n    questionBoxContent\n    questionBoxIcon\n    closedTimeout\n    closedMessage\n    disableCommenting\n    disableCommentingMessage\n    charCountEnable\n    charCount\n    requireEmailConfirmation\n    __typename\n  }\n  totalCommentCount @skip(if: $hasComment)\n  comments(query: {limit: 50, excludeIgnored: $excludeIgnored, sortOrder: $sortOrder, sortBy: $sortBy}) @skip(if: $hasComment) {\n    nodes {\n      ...CoralEmbedStream_Stream_comment\n      __typename\n    }\n    hasNextPage\n    startCursor\n    endCursor\n    __typename\n  }\n  ...TalkSlot_StreamTabsPrepend_asset\n  ...TalkSlot_StreamTabPanes_asset\n  ...TalkSlot_StreamFilter_asset\n  ...CoralEmbedStream_Comment_asset\n  __typename\n}\n\nfragment CoralEmbedStream_Comment_asset on Asset {\n  __typename\n  id\n  ...TalkSlot_CommentInfoBar_asset\n  ...TalkSlot_CommentActions_asset\n  ...TalkSlot_CommentReactions_asset\n  ...TalkSlot_CommentAuthorName_asset\n}\n\nfragment CoralEmbedStream_Stream_comment on Comment {\n  id\n  status\n  user {\n    id\n    __typename\n  }\n  ...CoralEmbedStream_Comment_comment\n  __typename\n}\n\nfragment CoralEmbedStream_Comment_comment on Comment {\n  ...CoralEmbedStream_Comment_SingleComment\n  replies(query: {limit: 3, excludeIgnored: $excludeIgnored}) {\n    nodes {\n      ...CoralEmbedStream_Comment_SingleComment\n      replies(query: {limit: 3, excludeIgnored: $excludeIgnored}) {\n        nodes {\n          ...CoralEmbedStream_Comment_SingleComment\n          replies(query: {limit: 3, excludeIgnored: $excludeIgnored}) {\n            nodes {\n              ...CoralEmbedStream_Comment_SingleComment\n              __typename\n            }\n            hasNextPage\n            startCursor\n            endCursor\n            __typename\n          }\n          __typename\n        }\n        hasNextPage\n        startCursor\n        endCursor\n        __typename\n      }\n      __typename\n    }\n    hasNextPage\n    startCursor\n    endCursor\n    __typename\n  }\n  __typename\n}\n\nfragment CoralEmbedStream_Comment_SingleComment on Comment {\n  id\n  body\n  created_at\n  status\n  replyCount\n  tags {\n    tag {\n      name\n      __typename\n    }\n    __typename\n  }\n  user {\n    id\n    username\n    __typename\n  }\n  status_history {\n    type\n    __typename\n  }\n  action_summaries {\n    __typename\n    count\n    current_user {\n      id\n      __typename\n    }\n  }\n  editing {\n    edited\n    editableUntil\n    __typename\n  }\n  ...TalkSlot_CommentInfoBar_comment\n  ...TalkSlot_CommentActions_comment\n  ...TalkSlot_CommentReactions_comment\n  ...TalkSlot_CommentAuthorName_comment\n  ...TalkSlot_CommentContent_comment\n  ...TalkEmbedStream_DraftArea_comment\n  ...TalkEmbedStream_DraftArea_comment\n  __typename\n}\n\nfragment TalkEmbedStream_DraftArea_comment on Comment {\n  __typename\n  ...TalkSlot_DraftArea_comment\n}\n\nfragment CoralEmbedStream_Stream_singleComment on Comment {\n  id\n  status\n  user {\n    id\n    __typename\n  }\n  ...CoralEmbedStream_Comment_SingleComment\n  __typename\n}\n\nfragment CoralEmbedStream_Configure_root on RootQuery {\n  __typename\n  ...CoralEmbedStream_Settings_root\n}\n\nfragment CoralEmbedStream_Settings_root on RootQuery {\n  __typename\n}\n\nfragment CoralEmbedStream_Configure_asset on Asset {\n  __typename\n  ...CoralEmbedStream_AssetStatusInfo_asset\n  ...CoralEmbedStream_Settings_asset\n}\n\nfragment CoralEmbedStream_AssetStatusInfo_asset on Asset {\n  id\n  closedAt\n  isClosed\n  __typename\n}\n\nfragment CoralEmbedStream_Settings_asset on Asset {\n  id\n  settings {\n    moderation\n    premodLinksEnable\n    questionBoxEnable\n    questionBoxIcon\n    questionBoxContent\n    __typename\n  }\n  __typename\n}\n\nfragment CoralEmbedStream_AutomaticAssetClosure_asset on Asset {\n  id\n  closedAt\n  __typename\n}\n\nfragment TalkSlot_StreamTabPanes_root on RootQuery {\n  ...TalkFeaturedComments_TabPane_root\n  __typename\n}\n\nfragment TalkFeaturedComments_TabPane_root on RootQuery {\n  __typename\n  ...TalkFeaturedComments_Comment_root\n}\n\nfragment TalkFeaturedComments_Comment_root on RootQuery {\n  __typename\n  ...TalkSlot_CommentAuthorName_root\n}\n\nfragment TalkSlot_StreamFilter_root on RootQuery {\n  ...TalkViewingOptions_ViewingOptions_root\n  __typename\n}\n\nfragment TalkViewingOptions_ViewingOptions_root on RootQuery {\n  __typename\n}\n\nfragment TalkSlot_CommentInfoBar_root on RootQuery {\n  ...TalkModerationActions_root\n  __typename\n}\n\nfragment TalkModerationActions_root on RootQuery {\n  me {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment TalkSlot_CommentAuthorName_root on RootQuery {\n  ...TalkAuthorMenu_AuthorName_root\n  __typename\n}\n\nfragment TalkAuthorMenu_AuthorName_root on RootQuery {\n  __typename\n  ...TalkSlot_AuthorMenuActions_root\n}\n\nfragment TalkSlot_StreamTabsPrepend_asset on Asset {\n  ...TalkFeaturedComments_Tab_asset\n  __typename\n}\n\nfragment TalkFeaturedComments_Tab_asset on Asset {\n  featuredCommentsCount: totalCommentCount(tags: [\"FEATURED\"]) @skip(if: $hasComment)\n  __typename\n}\n\nfragment TalkSlot_StreamTabPanes_asset on Asset {\n  ...TalkFeaturedComments_TabPane_asset\n  __typename\n}\n\nfragment TalkFeaturedComments_TabPane_asset on Asset {\n  id\n  featuredComments: comments(query: {tags: [\"FEATURED\"], sortOrder: $sortOrder, sortBy: $sortBy, excludeIgnored: $excludeIgnored}, deep: true) @skip(if: $hasComment) {\n    nodes {\n      ...TalkFeaturedComments_Comment_comment\n      __typename\n    }\n    hasNextPage\n    startCursor\n    endCursor\n    __typename\n  }\n  ...TalkFeaturedComments_Comment_asset\n  __typename\n}\n\nfragment TalkFeaturedComments_Comment_comment on Comment {\n  id\n  body\n  created_at\n  replyCount\n  tags {\n    tag {\n      name\n      __typename\n    }\n    __typename\n  }\n  user {\n    id\n    username\n    __typename\n  }\n  ...TalkSlot_CommentReactions_comment\n  ...TalkSlot_CommentAuthorName_comment\n  ...TalkSlot_CommentContent_comment\n  __typename\n}\n\nfragment TalkFeaturedComments_Comment_asset on Asset {\n  __typename\n  ...TalkSlot_CommentReactions_asset\n  ...TalkSlot_CommentAuthorName_asset\n}\n\nfragment TalkSlot_StreamFilter_asset on Asset {\n  ...TalkViewingOptions_ViewingOptions_asset\n  __typename\n}\n\nfragment TalkViewingOptions_ViewingOptions_asset on Asset {\n  __typename\n}\n\nfragment TalkSlot_CommentInfoBar_asset on Asset {\n  ...TalkModerationActions_asset\n  __typename\n}\n\nfragment TalkModerationActions_asset on Asset {\n  id\n  __typename\n}\n\nfragment TalkSlot_CommentActions_asset on Asset {\n  ...TalkPermalink_Button_asset\n  __typename\n}\n\nfragment TalkPermalink_Button_asset on Asset {\n  url\n  __typename\n}\n\nfragment TalkSlot_CommentReactions_asset on Asset {\n  ...RespectButton_asset\n  __typename\n}\n\nfragment RespectButton_asset on Asset {\n  id\n  __typename\n}\n\nfragment TalkSlot_CommentAuthorName_asset on Asset {\n  ...TalkAuthorMenu_AuthorName_asset\n  __typename\n}\n\nfragment TalkAuthorMenu_AuthorName_asset on Asset {\n  __typename\n}\n\nfragment TalkSlot_CommentInfoBar_comment on Comment {\n  ...TalkFeaturedComments_Tag_comment\n  ...TalkModerationActions_comment\n  __typename\n}\n\nfragment TalkFeaturedComments_Tag_comment on Comment {\n  tags {\n    tag {\n      name\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment TalkModerationActions_comment on Comment {\n  id\n  status\n  user {\n    id\n    __typename\n  }\n  tags {\n    tag {\n      name\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment TalkSlot_CommentActions_comment on Comment {\n  ...TalkPermalink_Button_comment\n  __typename\n}\n\nfragment TalkPermalink_Button_comment on Comment {\n  id\n  __typename\n}\n\nfragment TalkSlot_CommentReactions_comment on Comment {\n  ...RespectButton_comment\n  __typename\n}\n\nfragment RespectButton_comment on Comment {\n  id\n  action_summaries {\n    __typename\n    ... on RespectActionSummary {\n      count\n      current_user {\n        id\n        __typename\n      }\n      __typename\n    }\n  }\n  __typename\n}\n\nfragment TalkSlot_CommentAuthorName_comment on Comment {\n  ...TalkAuthorMenu_AuthorName_comment\n  __typename\n}\n\nfragment TalkAuthorMenu_AuthorName_comment on Comment {\n  __typename\n  id\n  user {\n    username\n    __typename\n  }\n  ...TalkSlot_AuthorMenuInfos_comment\n  ...TalkSlot_AuthorMenuActions_comment\n}\n\nfragment TalkSlot_CommentContent_comment on Comment {\n  ...TalkPluginRichText_CommentContent_comment\n  __typename\n}\n\nfragment TalkPluginRichText_CommentContent_comment on Comment {\n  body\n  richTextBody\n  __typename\n}\n\nfragment TalkSlot_DraftArea_comment on Comment {\n  ...TalkPluginRichText_Editor_comment\n  __typename\n}\n\nfragment TalkPluginRichText_Editor_comment on Comment {\n  body\n  richTextBody\n  __typename\n}\n\nfragment TalkSlot_AuthorMenuActions_root on RootQuery {\n  ...TalkIgnoreUser_IgnoreUserAction_root\n  __typename\n}\n\nfragment TalkIgnoreUser_IgnoreUserAction_root on RootQuery {\n  me {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment TalkSlot_AuthorMenuInfos_comment on Comment {\n  ...TalkMemberSince_MemberSinceInfo_comment\n  __typename\n}\n\nfragment TalkMemberSince_MemberSinceInfo_comment on Comment {\n  user {\n    username\n    created_at\n    __typename\n  }\n  __typename\n}\n\nfragment TalkSlot_AuthorMenuActions_comment on Comment {\n  ...TalkIgnoreUser_IgnoreUserAction_comment\n  __typename\n}\n\nfragment TalkIgnoreUser_IgnoreUserAction_comment on Comment {\n  user {\n    id\n    __typename\n  }\n  ...TalkIgnoreUser_IgnoreUserConfirmation_comment\n  __typename\n}\n\nfragment TalkIgnoreUser_IgnoreUserConfirmation_comment on Comment {\n  user {\n    id\n    username\n    __typename\n  }\n  __typename\n}\n","variables":{"assetId":"300200","assetUrl":"https://www.pagina12.com.ar/300200-elecciones-bolivia-2020-carlos-mesa-reconocio-la-derrota","commentId":"","hasComment":false,"excludeIgnored":false,"sortBy":"CREATED_AT","sortOrder":"DESC"},"operationName":"CoralEmbedStream_Embed"}'
    payload=json.loads(x)
    
    def get(self):
        url=self.url
        nota=r.get(url)
        sopa=bs(nota.content,features="lxml")
        ps=sopa.find('div','article-inner padding-right').findAll('p')
        st=sopa.find('div','article-inner padding-right').findAll('b')
        self.volanta=sopa.find('h2','article-prefix').text
        self.titulo=sopa.find('h1').text
        self.bajada=sopa.find('div','article-summary').text
        texto=list()
        for p in ps:
            texto.append(p.text)
        bolds=list()    
        for b in st:
            bolds.append(b.text)            
        self.bold=' '.join(bolds)
        self.bolds=bolds    
        self.cuerpo=' '.join(texto)
        aid=url.split('/')[-1].split('-')[0]
        payload=self.payload
        payload['variables']['assetId']=aid
        payload['variables']['assetUrl']=url
        
        pp=r.post("https://talk.pagina12.com.ar/api/v1/graph/ql", json=payload)
        self.coms=pp.json()['data']['asset']['comments']['nodes']
        self.comm=[x['body'] for x in self.coms]
        self.com=' '.join(self.comm)
        
        
class cronica():
    def __init__(self,url):
        self.url=url
   
    def get(self):
        ucr=self.url
        nota=r.get(ucr)
        sopa=bs(nota.content,features="lxml")
        self.volanta=None
        self.titulo=sopa.find('h1').text
        self.bajada=sopa.find('div',{'class' : 'title'}).text
        bolds=[x.text for x in sopa.find('div', { 'class' :"entry-body text-font"}).findAll('strong')]           
        self.bold=' '.join(bolds)
        self.bolds=bolds    
        self.cuerpo=sopa.find('div', { 'class' :"entry-body text-font"}).text        
        
        
class cronista():
    def __init__(self):
        self.url='https://www.cronista.com/'
   
    def get(self,url):
        
        nota=r.get(url)
        sopa=bs(nota.content,features="lxml")
        self.volanta=None
        self.titulo=sopa.find('h1').get_text(strip=True)
        self.bajada=sopa.find('p',{'class':'bajada'}).get_text(strip=True)
        bolds=[ unicodedata.normalize("NFKD",x.get_text(strip=True)) for x in sopa.find('div',{'class':"article-container"}).find_all('strong')]         
        self.bold=' '.join(bolds)
        self.bolds=bolds    
        self.cuerpo=''.join([unicodedata.normalize("NFKD",x.get_text().strip()) for x in sopa.find('div',{'class':"article-container"}).find_all('p') ]) 
        
    def hoy(self):
        url=self.url
        req=r.get(url)
        sopa=bs(req.content,features="lxml")
        titulos=sopa.find_all('h2',{'itemprop':"headline"})
        #urls=[url[:-1]+x.find('a').get('href') for x in titulos]
        urls=list()
        for x in titulos:
            if x.find('a').get('href')[:4] == 'http':
                urls.append(x.find('a').get('href'))
            else:
                urls.append(url[:-1]+x.find('a').get('href'))
            
        self.urls=urls
        
class dshow():
def __init__(self):
    self.url='https://www.diarioshow.com/'

def get(self,url):        
    nota=r.get(url)
    sopa=bs(nota.content,features="lxml")
    self.volanta=None
    self.titulo=sopa.find('h1').text
    self.bajada=unicodedata.normalize("NFKD",sopa.find('div',{'class' : 'title'}).get_text(strip=True))
    bolds=[unicodedata.normalize("NFKD",x.get_text(strip=True)) for x in sopa.find('div', { 'class' :"entry-body text-font"}).findAll('strong')]           
    self.bold=' / '.join(bolds)
    self.bolds=bolds   
    bulk=sopa.find('div', { 'class' :"entry-body text-font"}).find_all('p')
    self.cuerpo=''.join([unicodedata.normalize("NFKD",x.get_text()) for x in bulk])
    self.quotes=' / '.join([x.split('”')[0] for x in self.cuerpo.split('“')[1:]])       
        

class ibae():
    def __init__(self):
        self.url='https://www.infobae.com/'
   
    def get(self,url):        
        nota=r.get(url)
        sopa=bs(nota.content,features="lxml")
        self.titulo=sopa.find('h1').get_text(strip=True)
        self.bajada=sopa.find('h2').get_text(strip=True)
        mask=[ True  if x.find('mark',{'class':'hl_orange'}) else False for x in sopa.find('article').find_all('p')]
        ind=[i for i, x in enumerate(mask) if x == True][-1]
        self.cuerpo=' '.join([x.get_text() for x in sopa.find('article').find_all('p')[:ind]])
        self.bolds=[x.get_text(strip=True) for x in sopa.find('article').find_all('b')[:ind]][:-1]    
        self.bold=' / '.join(self.bolds)        
        self.quotes=' / '.join([x.split('”')[0] for x in self.cuerpo.split('“')[1:]])        

class ext():
    def __init__(self):
        self.url='https://exitoina.perfil.com/'
   
    def get(self,url):        
        nota=r.get(url)
        sopa=bs(nota.content,features="lxml")
        body=sopa.find('div',{'id':'news-body'})
        self.cuerpo=' '.join([unicodedata.normalize("NFKD",x.get_text()).strip() for x in body.find_all('p')])
        self.titulo=sopa.find('h1').text
        self.bajada=sopa.find('p','headline').text.strip()
        ps=body.find_all('p')
        bolds=[]
        for p in ps:
            bolds.extend([unicodedata.normalize("NFKD",x.get_text()).strip() for x in p.find_all('strong',recursive=False)])
        self.bolds=bolds
        self.quotes=[self.cuerpo.split('"')[1::2]]
        self.quot=' / '.join(self.cuerpo.split('"')[1::2])
        self.bold=' / '.join(bolds)