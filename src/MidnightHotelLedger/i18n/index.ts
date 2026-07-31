import type{Locale}from'../types';
export function detectLocale():Locale{const v=localStorage.getItem('game_locale');if(v==='zh'||v==='en')return v;return navigator.language.toLowerCase().startsWith('zh')?'zh':'en'}
const copy={
 zh:{hotel:'午夜酒店值班簿',subtitle:'异常住客也必须礼貌接待',start:'开始夜班',filed:'已归档',mute:'关闭声音',unmute:'开启声音',retry:'换个处置',continue:'继续值班',restart:'再值一次夜班',new:'新档案',seen:'已调阅',live:'事件录像',report:'夜班报告',choose:'千万别选正常答案',finalTitle:'夜班效率提升八倍',finalDetail:'章鱼同时接管电话、房卡、餐盘和服务铃。Mara 拿起外套下班，307号房的海水仍在流。'},
 en:{hotel:'THE MIDNIGHT HOTEL LEDGER',subtitle:'ABNORMAL GUESTS STILL REQUIRE PROPER SERVICE',start:'START NIGHT SHIFT',filed:'FILED',mute:'Mute sound',unmute:'Enable sound',retry:'TRY ANOTHER RESPONSE',continue:'CONTINUE SHIFT',restart:'WORK ANOTHER NIGHT',new:'NEW FILE',seen:'REVIEWED',live:'INCIDENT REEL',report:'NIGHT REPORT',choose:"DON’T PICK NORMAL",finalTitle:'NIGHT DESK EFFICIENCY ×8',finalDetail:'The octopus handles phone, keys, trays and bells at once. Mara clocks out while room 307 keeps leaking.'}
}as const;
export function t(locale:Locale,key:keyof typeof copy.zh){return copy[locale][key]}
