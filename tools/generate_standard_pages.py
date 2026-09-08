#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成标准页面（隐私政策/使用条款/联系我们/网站地图）的中英文版本
基于现有 cn/about.html 模板结构
"""

import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 页面内容定义
PAGES = {
    'privacy': {
        'cn': {
            'title': '009tg下海导航 - 隐私政策',
            'og_title': '009tg下海导航 - 隐私政策',
            'og_desc': '009tg下海导航 - 隐私政策，了解我们如何保护您的隐私。',
            'heading': '隐私政策',
            'content': '''
                    <blockquote>
                        <p>009tg下海导航（以下简称"本网站"）非常重视用户的隐私保护。本隐私政策旨在说明我们如何收集、使用、存储和保护您的个人信息。</p>
                    </blockquote>
                    <h5>一、信息收集</h5>
                    <p>本网站在您访问时可能收集以下信息：</p>
                    <ul>
                        <li>浏览器类型和版本</li>
                        <li>操作系统类型</li>
                        <li>访问时间和页面浏览记录</li>
                        <li>IP地址（用于统计分析，不与个人身份关联）</li>
                        <li>Cookie信息（用于改善用户体验）</li>
                    </ul>
                    <h5>二、信息使用</h5>
                    <p>收集的信息仅用于以下目的：</p>
                    <ul>
                        <li>改善网站内容和用户体验</li>
                        <li>统计网站访问量和用户行为分析</li>
                        <li>展示个性化广告（通过Google AdSense等第三方广告平台）</li>
                        <li>网站维护和安全防护</li>
                    </ul>
                    <h5>三、Cookie使用</h5>
                    <p>本网站使用Cookie来改善用户体验。Cookie是存储在您浏览器中的小型文本文件，用于记住您的偏好设置。您可以通过浏览器设置禁用Cookie，但这可能影响网站的部分功能。</p>
                    <p>第三方广告商（如Google）可能使用Cookie来展示基于您访问记录的广告。您可以通过访问Google广告设置页面来管理个性化广告偏好。</p>
                    <h5>四、第三方服务</h5>
                    <p>本网站使用以下第三方服务：</p>
                    <ul>
                        <li><strong>Google AdSense</strong>：用于展示广告，可能收集您的浏览信息</li>
                        <li><strong>百度统计</strong>：用于网站访问统计分析</li>
                        <li><strong>Cloudflare</strong>：用于CDN加速和安全防护</li>
                    </ul>
                    <p>这些第三方服务有各自的隐私政策，本网站不对其隐私做法负责。</p>
                    <h5>五、信息保护</h5>
                    <p>我们采取合理的技术和管理措施来保护您的信息安全，包括但不限于数据加密、访问控制和安全审计。但请注意，互联网传输无法保证100%安全。</p>
                    <h5>六、政策更新</h5>
                    <p>本隐私政策可能会不时更新。更新后的政策将在本页面发布，重大变更时我们会在网站首页显著位置通知。</p>
                    <h5>七、联系我们</h5>
                    <p>如对本隐私政策有任何疑问，请通过<a href="contact.html">联系我们</a>页面与我们取得联系。</p>
                    <p><em>最后更新日期：2026年9月</em></p>
'''
        },
        'en': {
            'title': '009tg Navigation - Privacy Policy',
            'og_title': '009tg Navigation - Privacy Policy',
            'og_desc': '009tg Navigation - Privacy Policy, learn how we protect your privacy.',
            'heading': 'Privacy Policy',
            'content': '''
                    <blockquote>
                        <p>009tg Navigation (hereinafter referred to as "this website") takes user privacy protection very seriously. This Privacy Policy explains how we collect, use, store, and protect your personal information.</p>
                    </blockquote>
                    <h5>1. Information Collection</h5>
                    <p>This website may collect the following information when you visit:</p>
                    <ul>
                        <li>Browser type and version</li>
                        <li>Operating system type</li>
                        <li>Access time and page browsing history</li>
                        <li>IP address (for statistical analysis, not linked to personal identity)</li>
                        <li>Cookie information (to improve user experience)</li>
                    </ul>
                    <h5>2. Information Use</h5>
                    <p>Collected information is used only for the following purposes:</p>
                    <ul>
                        <li>Improving website content and user experience</li>
                        <li>Website traffic statistics and user behavior analysis</li>
                        <li>Displaying personalized ads (through third-party ad platforms like Google AdSense)</li>
                        <li>Website maintenance and security protection</li>
                    </ul>
                    <h5>3. Cookie Usage</h5>
                    <p>This website uses cookies to improve user experience. Cookies are small text files stored in your browser to remember your preferences. You can disable cookies through your browser settings, but this may affect some website features.</p>
                    <p>Third-party advertisers (such as Google) may use cookies to display ads based on your visit history. You can manage personalized ad preferences by visiting the Google Ads Settings page.</p>
                    <h5>4. Third-Party Services</h5>
                    <p>This website uses the following third-party services:</p>
                    <ul>
                        <li><strong>Google AdSense</strong>: For displaying ads, may collect your browsing information</li>
                        <li><strong>Baidu Analytics</strong>: For website traffic statistics and analysis</li>
                        <li><strong>Cloudflare</strong>: For CDN acceleration and security protection</li>
                    </ul>
                    <p>These third-party services have their own privacy policies, and this website is not responsible for their privacy practices.</p>
                    <h5>5. Information Protection</h5>
                    <p>We take reasonable technical and administrative measures to protect your information security, including but not limited to data encryption, access control, and security audits. Please note, however, that internet transmission cannot guarantee 100% security.</p>
                    <h5>6. Policy Updates</h5>
                    <p>This Privacy Policy may be updated from time to time. The updated policy will be posted on this page, and for major changes, we will notify you prominently on the website homepage.</p>
                    <h5>7. Contact Us</h5>
                    <p>If you have any questions about this Privacy Policy, please contact us through the <a href="contact.html">Contact Us</a> page.</p>
                    <p><em>Last updated: September 2026</em></p>
'''
        }
    },
    'terms': {
        'cn': {
            'title': '009tg下海导航 - 使用条款',
            'og_title': '009tg下海导航 - 使用条款',
            'og_desc': '009tg下海导航 - 使用条款，了解使用本网站的规则和条件。',
            'heading': '使用条款',
            'content': '''
                    <blockquote>
                        <p>欢迎使用009tg下海导航（以下简称"本网站"）。在使用本网站前，请仔细阅读以下使用条款。使用本网站即表示您同意遵守这些条款。</p>
                    </blockquote>
                    <h5>一、服务内容</h5>
                    <p>本网站是一个网址导航平台，收集和整理互联网上的各类实用网站和工具，为用户提供便捷的网址导航服务。本网站不直接提供这些外部网站的内容和服务，仅提供链接跳转。</p>
                    <h5>二、用户行为规范</h5>
                    <p>使用本网站时，您同意：</p>
                    <ul>
                        <li>遵守中华人民共和国相关法律法规</li>
                        <li>不利用本网站从事任何违法违规活动</li>
                        <li>不攻击、干扰本网站的正常运行</li>
                        <li>不恶意爬取、复制本网站内容</li>
                        <li>不传播病毒、恶意代码或其他有害程序</li>
                    </ul>
                    <h5>三、外部链接免责</h5>
                    <p>本网站包含大量指向第三方网站的外部链接。这些链接仅为方便用户而提供，本网站不对外部网站的内容、准确性、合法性、安全性或隐私政策负责。您访问外部网站所产生的任何风险由您自行承担。</p>
                    <p>如您发现本网站收录的链接存在违法违规或侵权内容，请通过<a href="contact.html">联系我们</a>页面告知，我们将及时处理。</p>
                    <h5>四、知识产权</h5>
                    <p>本网站的原创内容（包括但不限于网站设计、文字描述、分类体系）受知识产权法律保护。未经书面授权，不得复制、转载、修改或用于商业用途。</p>
                    <p>本网站收录的外部网站名称、Logo、描述等内容归各自所有者所有。如认为本网站收录侵犯了您的权益，请联系我们处理。</p>
                    <h5>五、服务变更与终止</h5>
                    <p>本网站有权根据需要随时变更、暂停或终止部分或全部服务，无需事先通知。因服务变更或终止给您造成的影响，本网站不承担责任。</p>
                    <h5>六、免责声明</h5>
                    <p>在法律允许的最大范围内，本网站不对因使用或无法使用本网站而产生的任何直接、间接、附带、特殊或后果性损失承担责任，包括但不限于利润损失、数据丢失、业务中断等。</p>
                    <h5>七、条款修改</h5>
                    <p>本网站有权随时修改本使用条款。修改后的条款将在本页面发布，继续使用本网站即表示您接受修改后的条款。</p>
                    <h5>八、法律适用</h5>
                    <p>本使用条款的解释、执行和争议解决均适用中华人民共和国法律。如发生争议，双方应友好协商解决；协商不成的，可向本网站运营者所在地人民法院提起诉讼。</p>
                    <p><em>最后更新日期：2026年9月</em></p>
'''
        },
        'en': {
            'title': '009tg Navigation - Terms of Service',
            'og_title': '009tg Navigation - Terms of Service',
            'og_desc': '009tg Navigation - Terms of Service, understand the rules and conditions for using this website.',
            'heading': 'Terms of Service',
            'content': '''
                    <blockquote>
                        <p>Welcome to 009tg Navigation (hereinafter referred to as "this website"). Before using this website, please carefully read the following Terms of Service. By using this website, you agree to comply with these terms.</p>
                    </blockquote>
                    <h5>1. Service Content</h5>
                    <p>This website is a URL navigation platform that collects and organizes various practical websites and tools on the internet, providing users with convenient URL navigation services. This website does not directly provide the content and services of these external websites, but only provides link redirection.</p>
                    <h5>2. User Conduct</h5>
                    <p>When using this website, you agree to:</p>
                    <ul>
                        <li>Comply with relevant laws and regulations</li>
                        <li>Not use this website for any illegal activities</li>
                        <li>Not attack or interfere with the normal operation of this website</li>
                        <li>Not maliciously crawl or copy website content</li>
                        <li>Not spread viruses, malicious code, or other harmful programs</li>
                    </ul>
                    <h5>3. External Links Disclaimer</h5>
                    <p>This website contains numerous external links to third-party websites. These links are provided solely for user convenience. This website is not responsible for the content, accuracy, legality, security, or privacy policies of external websites. Any risks arising from your access to external websites are borne by you alone.</p>
                    <p>If you find that links included on this website contain illegal, infringing, or inappropriate content, please notify us through the <a href="contact.html">Contact Us</a> page, and we will promptly address it.</p>
                    <h5>4. Intellectual Property</h5>
                    <p>Original content of this website (including but not limited to website design, text descriptions, classification system) is protected by intellectual property laws. Without written authorization, no copying, reproduction, modification, or commercial use is permitted.</p>
                    <p>External website names, logos, descriptions, and other content included on this website belong to their respective owners. If you believe that inclusion on this website infringes your rights, please contact us for resolution.</p>
                    <h5>5. Service Changes and Termination</h5>
                    <p>This website reserves the right to change, suspend, or terminate part or all of its services at any time as needed, without prior notice. This website shall not be liable for any impact caused by service changes or termination.</p>
                    <h5>6. Disclaimer</h5>
                    <p>To the maximum extent permitted by law, this website shall not be liable for any direct, indirect, incidental, special, or consequential damages arising from the use or inability to use this website, including but not limited to loss of profits, data loss, business interruption, etc.</p>
                    <h5>7. Terms Modification</h5>
                    <p>This website reserves the right to modify these Terms of Service at any time. Modified terms will be posted on this page. Continued use of this website constitutes your acceptance of the modified terms.</p>
                    <h5>8. Governing Law</h5>
                    <p>The interpretation, execution, and dispute resolution of these Terms of Service shall be governed by the laws of the People's Republic of China. In case of disputes, both parties shall resolve them through friendly negotiation; if negotiation fails, a lawsuit may be filed with the People's Court at the location of the website operator.</p>
                    <p><em>Last updated: September 2026</em></p>
'''
        }
    },
    'disclaimer': {
        'cn': {
            'title': '009tg下海导航 - 免责声明',
            'og_title': '009tg下海导航 - 免责声明',
            'og_desc': '009tg下海导航 - 免责声明，了解本站的责任边界和使用须知。',
            'heading': '免责声明',
            'content': '''
                    <blockquote>
                        <p>欢迎使用009tg下海导航（以下简称"本网站"）。在使用本网站前，请仔细阅读以下免责声明。您的使用行为即视为同意本声明的全部条款。</p>
                    </blockquote>
                    <h5>一、网站性质</h5>
                    <p>本网站是一个网址导航平台，旨在为用户提供便捷的网站分类索引和资源聚合服务。本网站收录的所有外部网站链接均来自公开网络，仅作为用户获取信息的参考，不代表本网站对其内容的真实性、准确性、合法性或可靠性作出任何保证或承诺。</p>
                    <h5>二、外部链接免责</h5>
                    <p>本网站包含大量指向第三方网站的链接。对于这些外部网站的内容、隐私政策、服务质量或任何其他方面，本网站不承担任何责任。用户通过本网站链接访问第三方网站时，应自行承担风险，并仔细阅读该网站的用户协议和隐私政策。</p>
                    <p>本网站不对外部链接的可用性、及时性、安全性作出保证。如发现链接失效或指向不当内容，请通过<a href="contact.html">联系我们</a>页面告知，我们将及时处理。</p>
                    <h5>三、内容免责</h5>
                    <p>本网站展示的站点名称、描述、图标等信息，部分来源于被收录网站的公开元数据（如meta标签），部分由用户或编辑提交。本网站尽力确保信息的准确性，但不对信息的完整性、准确性、时效性作出保证。</p>
                    <p>本网站的文章和指南内容仅供参考和学习交流，不构成任何投资建议、法律意见或专业指导。用户据此操作所产生的任何后果，本网站不承担责任。</p>
                    <h5>四、知识产权</h5>
                    <p>本网站的原创内容（包括但不限于文章、分类体系、页面设计）受知识产权法律保护。未经授权，不得复制、转载或用于商业用途。</p>
                    <p>本网站收录的站点名称、logo、描述等归各自权利人所有。如权利人认为本网站的收录侵犯了其合法权益，请通过<a href="contact.html">联系我们</a>页面提供权属证明，我们将在核实后及时处理。</p>
                    <h5>五、用户行为</h5>
                    <p>用户在使用本网站时应遵守相关法律法规，不得利用本网站从事任何违法违规活动。用户因自身行为导致的任何法律责任，由用户自行承担。</p>
                    <h5>六、服务变更与终止</h5>
                    <p>本网站有权根据实际情况随时调整、暂停或终止部分或全部服务，且无需事先通知用户。本网站不对服务的中断或终止承担任何责任。</p>
                    <h5>七、免责声明更新</h5>
                    <p>本免责声明可能会不时更新。更新后的声明将在本页面发布，继续使用本网站即视为接受更新后的声明。</p>
                    <h5>八、联系我们</h5>
                    <p>如对本免责声明有任何疑问，或需要投诉举报相关内容，请通过<a href="contact.html">联系我们</a>页面与我们取得联系。</p>
                    <p><em>最后更新日期：2026年9月</em></p>
'''
        },
        'en': {
            'title': '009tg Navigation - Disclaimer',
            'og_title': '009tg Navigation - Disclaimer',
            'og_desc': '009tg Navigation - Disclaimer, understand our liability boundaries and terms of use.',
            'heading': 'Disclaimer',
            'content': '''
                    <blockquote>
                        <p>Welcome to 009tg Navigation (hereinafter referred to as "this website"). Before using this website, please carefully read the following disclaimer. Your use of this website constitutes agreement to all terms of this disclaimer.</p>
                    </blockquote>
                    <h5>1. Website Nature</h5>
                    <p>This website is a URL navigation platform designed to provide users with convenient website classification indexing and resource aggregation services. All external website links included on this website come from the public Internet and are only provided as a reference for users to obtain information. This website does not guarantee or promise the authenticity, accuracy, legality, or reliability of their content.</p>
                    <h5>2. External Links Disclaimer</h5>
                    <p>This website contains numerous links to third-party websites. This website is not responsible for the content, privacy policies, service quality, or any other aspects of these external websites. When users access third-party websites through links on this website, they do so at their own risk and should carefully read the user agreement and privacy policy of that website.</p>
                    <p>This website does not guarantee the availability, timeliness, or security of external links. If you find a broken link or a link pointing to inappropriate content, please notify us through the <a href="contact.html">Contact Us</a> page, and we will promptly address it.</p>
                    <h5>3. Content Disclaimer</h5>
                    <p>The site names, descriptions, icons, and other information displayed on this website are partially derived from the public metadata of the listed websites (such as meta tags) and partially submitted by users or editors. This website strives to ensure the accuracy of the information but does not guarantee its completeness, accuracy, or timeliness.</p>
                    <p>The articles and guides on this website are for reference and learning exchange only and do not constitute any investment advice, legal opinion, or professional guidance. This website is not responsible for any consequences arising from users' operations based on this information.</p>
                    <h5>4. Intellectual Property</h5>
                    <p>The original content of this website (including but not limited to articles, classification systems, and page design) is protected by intellectual property laws. Unauthorized copying, reproduction, or commercial use is prohibited.</p>
                    <p>The site names, logos, descriptions, etc., listed on this website belong to their respective rights holders. If a rights holder believes that the listing on this website infringes upon their legitimate rights and interests, please provide proof of ownership through the <a href="contact.html">Contact Us</a> page, and we will promptly address it after verification.</p>
                    <h5>5. User Behavior</h5>
                    <p>Users should comply with relevant laws and regulations when using this website and must not use this website to engage in any illegal activities. Users shall bear any legal liabilities arising from their own actions.</p>
                    <h5>6. Service Changes and Termination</h5>
                    <p>This website reserves the right to adjust, suspend, or terminate part or all of its services at any time based on actual conditions without prior notice to users. This website shall not be liable for any interruption or termination of services.</p>
                    <h5>7. Disclaimer Updates</h5>
                    <p>This disclaimer may be updated from time to time. The updated disclaimer will be published on this page, and continued use of this website constitutes acceptance of the updated disclaimer.</p>
                    <h5>8. Contact Us</h5>
                    <p>If you have any questions about this disclaimer, or need to report related content, please contact us through the <a href="contact.html">Contact Us</a> page.</p>
                    <p><em>Last updated: September 2026</em></p>
'''
        }
    },
    'contact': {
        'cn': {
            'title': '009tg下海导航 - 联系我们',
            'og_title': '009tg下海导航 - 联系我们',
            'og_desc': '009tg下海导航 - 联系我们，如有问题或建议请与我们取得联系。',
            'heading': '联系我们',
            'content': '''
                    <blockquote>
                        <p>感谢您访问009tg下海导航！如果您有任何问题、建议、合作意向或需要举报无效链接，欢迎通过以下方式与我们联系。</p>
                    </blockquote>
                    <h5>联系方式</h5>
                    <div class="row">
                        <div class="col-sm-6">
                            <div class="panel panel-default">
                                <div class="panel-body">
                                    <h5><i class="fa-envelope"></i> 电子邮件</h5>
                                    <p>商务合作 / 广告投放：<a href="mailto:invisibleman009tg@proton.me">invisibleman009tg@proton.me</a></p>
                                    <p>问题反馈 / 建议：<a href="mailto:invisibleman009tg@proton.me">invisibleman009tg@proton.me</a></p>
                                    <p>无效链接举报：<a href="mailto:invisibleman009tg@proton.me">invisibleman009tg@proton.me</a></p>
                                </div>
                            </div>
                        </div>
                        <div class="col-sm-6">
                            <div class="panel panel-default">
                                <div class="panel-body">
                                    <h5><i class="fa-clock-o"></i> 响应时间</h5>
                                    <p>工作日：通常在24小时内回复</p>
                                    <p>周末/节假日：可能延迟至下一个工作日</p>
                                    <p>紧急事项：请在邮件标题标注【紧急】</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <h5>常见问题</h5>
                    <div class="panel-group" id="accordion">
                        <div class="panel panel-default">
                            <div class="panel-heading">
                                <h5 class="panel-title">
                                    <a data-toggle="collapse" data-parent="#accordion" href="#collapse1">如何提交新网站？</a>
                                </h5>
                            </div>
                            <div id="collapse1" class="panel-collapse collapse">
                                <div class="panel-body">
                                    <p>请发送邮件至 <a href="mailto:invisibleman009tg@proton.me">invisibleman009tg@proton.me</a>，邮件中请包含：网站名称、网址、网站简介、所属分类建议。我们会在审核后决定是否收录。</p>
                                </div>
                            </div>
                        </div>
                        <div class="panel panel-default">
                            <div class="panel-heading">
                                <h5 class="panel-title">
                                    <a data-toggle="collapse" data-parent="#accordion" href="#collapse2">如何举报无效链接？</a>
                                </h5>
                            </div>
                            <div id="collapse2" class="panel-collapse collapse">
                                <div class="panel-body">
                                    <p>请发送邮件至 <a href="mailto:invisibleman009tg@proton.me">invisibleman009tg@proton.me</a>，邮件中请包含：无效链接的网站名称、网址、具体问题（无法访问/内容不符/已改版等）。我们会尽快核实并处理。</p>
                                </div>
                            </div>
                        </div>
                        <div class="panel panel-default">
                            <div class="panel-heading">
                                <h5 class="panel-title">
                                    <a data-toggle="collapse" data-parent="#accordion" href="#collapse3">广告合作方式？</a>
                                </h5>
                            </div>
                            <div id="collapse3" class="panel-collapse collapse">
                                <div class="panel-body">
                                    <p>我们提供多种广告合作方式，包括首页横幅广告、分类页广告、推荐位等。具体报价和方案请发送邮件至 <a href="mailto:invisibleman009tg@proton.me">invisibleman009tg@proton.me</a> 咨询。</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <h5>注意事项</h5>
                    <ul>
                        <li>请在邮件中清晰描述您的问题或需求，以便我们更快地处理</li>
                        <li>涉及网站收录的邮件，请确保网站内容合法合规</li>
                        <li>我们不接受任何形式的付费收录请求，所有收录均基于网站质量</li>
                        <li>如未收到回复，请检查垃圾邮件文件夹或再次发送</li>
                    </ul>
'''
        },
        'en': {
            'title': '009tg Navigation - Contact Us',
            'og_title': '009tg Navigation - Contact Us',
            'og_desc': '009tg Navigation - Contact Us, reach out to us with any questions or suggestions.',
            'heading': 'Contact Us',
            'content': '''
                    <blockquote>
                        <p>Thank you for visiting 009tg Navigation! If you have any questions, suggestions, partnership inquiries, or need to report invalid links, please feel free to contact us through the following methods.</p>
                    </blockquote>
                    <h5>Contact Information</h5>
                    <div class="row">
                        <div class="col-sm-6">
                            <div class="panel panel-default">
                                <div class="panel-body">
                                    <h5><i class="fa-envelope"></i> Email</h5>
                                    <p>Business / Advertising: <a href="mailto:invisibleman009tg@proton.me">invisibleman009tg@proton.me</a></p>
                                    <p>Feedback / Suggestions: <a href="mailto:invisibleman009tg@proton.me">invisibleman009tg@proton.me</a></p>
                                    <p>Invalid Link Reports: <a href="mailto:invisibleman009tg@proton.me">invisibleman009tg@proton.me</a></p>
                                </div>
                            </div>
                        </div>
                        <div class="col-sm-6">
                            <div class="panel panel-default">
                                <div class="panel-body">
                                    <h5><i class="fa-clock-o"></i> Response Time</h5>
                                    <p>Business days: Usually within 24 hours</p>
                                    <p>Weekends/Holidays: May be delayed to next business day</p>
                                    <p>Urgent matters: Please mark 【URGENT】 in email subject</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <h5>FAQ</h5>
                    <div class="panel-group" id="accordion">
                        <div class="panel panel-default">
                            <div class="panel-heading">
                                <h5 class="panel-title">
                                    <a data-toggle="collapse" data-parent="#accordion" href="#collapse1">How to submit a new website?</a>
                                </h5>
                            </div>
                            <div id="collapse1" class="panel-collapse collapse">
                                <div class="panel-body">
                                    <p>Please send an email to <a href="mailto:invisibleman009tg@proton.me">invisibleman009tg@proton.me</a> with: website name, URL, brief description, and suggested category. We will review and decide whether to include it.</p>
                                </div>
                            </div>
                        </div>
                        <div class="panel panel-default">
                            <div class="panel-heading">
                                <h5 class="panel-title">
                                    <a data-toggle="collapse" data-parent="#accordion" href="#collapse2">How to report an invalid link?</a>
                                </h5>
                            </div>
                            <div id="collapse2" class="panel-collapse collapse">
                                <div class="panel-body">
                                    <p>Please send an email to <a href="mailto:invisibleman009tg@proton.me">invisibleman009tg@proton.me</a> with: the website name, URL, and specific issue (inaccessible/content mismatch/redesigned, etc.). We will verify and address it promptly.</p>
                                </div>
                            </div>
                        </div>
                        <div class="panel panel-default">
                            <div class="panel-heading">
                                <h5 class="panel-title">
                                    <a data-toggle="collapse" data-parent="#accordion" href="#collapse3">Advertising partnership options?</a>
                                </h5>
                            </div>
                            <div id="collapse3" class="panel-collapse collapse">
                                <div class="panel-body">
                                    <p>We offer various advertising partnership options, including homepage banner ads, category page ads, featured positions, etc. For specific pricing and plans, please email <a href="mailto:invisibleman009tg@proton.me">invisibleman009tg@proton.me</a>.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <h5>Notes</h5>
                    <ul>
                        <li>Please clearly describe your question or request in the email so we can process it faster</li>
                        <li>For website inclusion requests, please ensure the website content is legal and compliant</li>
                        <li>We do not accept any form of paid inclusion requests; all inclusions are based on website quality</li>
                        <li>If you do not receive a reply, please check your spam folder or resend</li>
                    </ul>
'''
        }
    },
    'sitemap': {
        'cn': {
            'title': '009tg下海导航 - 网站地图',
            'og_title': '009tg下海导航 - 网站地图',
            'og_desc': '009tg下海导航 - 网站地图，快速浏览所有分类和页面。',
            'heading': '网站地图',
            'content': '''
                    <blockquote>
                        <p>本页面列出了009tg下海导航的所有主要分类和页面，方便您快速浏览和查找所需内容。</p>
                    </blockquote>
                    <h5>主要页面</h5>
                    <div class="row">
                        <div class="col-sm-4">
                            <ul class="list-group">
                                <li class="list-group-item"><a href="../index.html"><i class="fa-home"></i> 首页</a></li>
                                <li class="list-group-item"><a href="about.html"><i class="fa-info-circle"></i> 关于本站</a></li>
                                <li class="list-group-item"><a href="privacy.html"><i class="fa-lock"></i> 隐私政策</a></li>
                                <li class="list-group-item"><a href="terms.html"><i class="fa-file-text"></i> 使用条款</a></li>
                                <li class="list-group-item"><a href="contact.html"><i class="fa-envelope"></i> 联系我们</a></li>
                            </ul>
                        </div>
                        <div class="col-sm-4">
                            <ul class="list-group">
                                <li class="list-group-item"><a href="../sitemap.xml"><i class="fa-sitemap"></i> XML Sitemap</a></li>
                                <li class="list-group-item"><a href="../404.html"><i class="fa-exclamation-triangle"></i> 404页面</a></li>
                                <li class="list-group-item"><a href="../redirect.html"><i class="fa-external-link"></i> 跳转页面</a></li>
                            </ul>
                        </div>
                    </div>
                    <h5>网站分类</h5>
                    <p>本站收录了超过2400个实用网站，涵盖以下主要分类：</p>
                    <div class="row">
                        <div class="col-sm-6">
                            <ul>
                                <li><strong>下海推荐</strong> - 精选实用工具和常用网址</li>
                                <li><strong>AI工具</strong> - 人工智能相关工具和平台</li>
                                <li><strong>跨境资讯</strong> - 跨境电商行业新闻和资讯</li>
                                <li><strong>跨境推广</strong> - 海外营销和推广工具</li>
                                <li><strong>社媒资源</strong> - 社交媒体运营资源</li>
                                <li><strong>全球网络</strong> - VPN、代理、网络加速</li>
                                <li><strong>全球接码</strong> - 海外手机号接码平台</li>
                                <li><strong>数字货币</strong> - 加密货币交易和钱包</li>
                                <li><strong>全球支付</strong> - 国际支付和收款工具</li>
                                <li><strong>Facebook</strong> - Facebook营销和运营工具</li>
                            </ul>
                        </div>
                        <div class="col-sm-6">
                            <ul>
                                <li><strong>Google</strong> - Google工具和服务</li>
                                <li><strong>广告工具</strong> - 广告投放和优化工具</li>
                                <li><strong>指纹浏览器</strong> - 反检测浏览器和指纹工具</li>
                                <li><strong>全球APP下载</strong> - 海外应用下载资源</li>
                                <li><strong>内容制作</strong> - 图文视频内容创作工具</li>
                                <li><strong>技术交流</strong> - 技术论坛和社区</li>
                                <li><strong>引流工具</strong> - 流量获取和转化工具</li>
                                <li><strong>跨境电商</strong> - 电商平台和运营工具</li>
                                <li><strong>跨境服务</strong> - 物流、仓储、代运营服务</li>
                            </ul>
                        </div>
                    </div>
                    <h5>快速导航</h5>
                    <p>返回<a href="../index.html">首页</a>浏览所有网站，或使用左侧菜单按分类查看。</p>
'''
        },
        'en': {
            'title': '009tg Navigation - Sitemap',
            'og_title': '009tg Navigation - Sitemap',
            'og_desc': '009tg Navigation - Sitemap, quickly browse all categories and pages.',
            'heading': 'Sitemap',
            'content': '''
                    <blockquote>
                        <p>This page lists all major categories and pages of 009tg Navigation for your quick browsing and convenience.</p>
                    </blockquote>
                    <h5>Main Pages</h5>
                    <div class="row">
                        <div class="col-sm-4">
                            <ul class="list-group">
                                <li class="list-group-item"><a href="../index.html"><i class="fa-home"></i> Homepage</a></li>
                                <li class="list-group-item"><a href="about.html"><i class="fa-info-circle"></i> About Us</a></li>
                                <li class="list-group-item"><a href="privacy.html"><i class="fa-lock"></i> Privacy Policy</a></li>
                                <li class="list-group-item"><a href="terms.html"><i class="fa-file-text"></i> Terms of Service</a></li>
                                <li class="list-group-item"><a href="contact.html"><i class="fa-envelope"></i> Contact Us</a></li>
                            </ul>
                        </div>
                        <div class="col-sm-4">
                            <ul class="list-group">
                                <li class="list-group-item"><a href="../sitemap.xml"><i class="fa-sitemap"></i> XML Sitemap</a></li>
                                <li class="list-group-item"><a href="../404.html"><i class="fa-exclamation-triangle"></i> 404 Page</a></li>
                                <li class="list-group-item"><a href="../redirect.html"><i class="fa-external-link"></i> Redirect Page</a></li>
                            </ul>
                        </div>
                    </div>
                    <h5>Website Categories</h5>
                    <p>This site includes over 2400 practical websites covering the following main categories:</p>
                    <div class="row">
                        <div class="col-sm-6">
                            <ul>
                                <li><strong>Featured</strong> - Curated practical tools and popular URLs</li>
                                <li><strong>AI Tools</strong> - Artificial intelligence tools and platforms</li>
                                <li><strong>Cross-border News</strong> - Cross-border e-commerce industry news</li>
                                <li><strong>Cross-border Marketing</strong> - Overseas marketing and promotion tools</li>
                                <li><strong>Social Media</strong> - Social media operation resources</li>
                                <li><strong>Global Network</strong> - VPN, proxy, network acceleration</li>
                                <li><strong>SMS Verification</strong> - Overseas phone number verification</li>
                                <li><strong>Crypto</strong> - Cryptocurrency trading and wallets</li>
                                <li><strong>Global Payment</strong> - International payment and collection tools</li>
                                <li><strong>Facebook</strong> - Facebook marketing and operation tools</li>
                            </ul>
                        </div>
                        <div class="col-sm-6">
                            <ul>
                                <li><strong>Google</strong> - Google tools and services</li>
                                <li><strong>Ad Tools</strong> - Ad placement and optimization tools</li>
                                <li><strong>Antidetect Browser</strong> - Anti-detect browsers and fingerprint tools</li>
                                <li><strong>Global Apps</strong> - Overseas app download resources</li>
                                <li><strong>Content Creation</strong> - Image, text, video creation tools</li>
                                <li><strong>Tech Community</strong> - Technical forums and communities</li>
                                <li><strong>Traffic Tools</strong> - Traffic acquisition and conversion tools</li>
                                <li><strong>E-commerce</strong> - E-commerce platforms and operation tools</li>
                                <li><strong>Cross-border Services</strong> - Logistics, warehousing, agency services</li>
                            </ul>
                        </div>
                    </div>
                    <h5>Quick Navigation</h5>
                    <p>Return to the <a href="../index.html">Homepage</a> to browse all websites, or use the sidebar menu to view by category.</p>
'''
        }
    }
}


def generate_page(page_key, lang):
    """生成单个页面"""
    page = PAGES[page_key][lang]
    lang_prefix = '../'  # cn/ 和 en/ 目录都用 ../ 引用根目录资源

    # 语言切换链接
    if lang == 'cn':
        lang_switcher = '''
                    <li class="dropdown hover-line language-switcher">
                        <a href="index.html" class="dropdown-toggle" data-toggle="dropdown">
                            <img src="''' + lang_prefix + '''assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese
                        </a>
                        <ul class="dropdown-menu languages">
                            <li>
                                <a href="../en/''' + page_key + '''.html">
                                    <img src="''' + lang_prefix + '''assets/images/flags/flag-us.png" alt="flag-us" /> English
                                </a>
                            </li>
                            <li class="active">
                                <a href="../cn/''' + page_key + '''.html">
                                    <img src="''' + lang_prefix + '''assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese
                                </a>
                            </li>
                        </ul>
                    </li>'''
        html_lang = 'zh'
    else:
        lang_switcher = '''
                    <li class="dropdown hover-line language-switcher">
                        <a href="index.html" class="dropdown-toggle" data-toggle="dropdown">
                            <img src="''' + lang_prefix + '''assets/images/flags/flag-us.png" alt="flag-us" /> English
                        </a>
                        <ul class="dropdown-menu languages">
                            <li class="active">
                                <a href="../en/''' + page_key + '''.html">
                                    <img src="''' + lang_prefix + '''assets/images/flags/flag-us.png" alt="flag-us" /> English
                                </a>
                            </li>
                            <li>
                                <a href="../cn/''' + page_key + '''.html">
                                    <img src="''' + lang_prefix + '''assets/images/flags/flag-cn.png" alt="flag-cn" /> Chinese
                                </a>
                            </li>
                        </ul>
                    </li>'''
        html_lang = 'en'

    # 底部footer内容
    if lang == 'cn':
        footer_html = f'''<footer class="site-footer">
        <div class="footer-container">
            <div class="footer-links">
                <a href="index.html">首页</a>
                <a href="about.html">关于我们</a>
                <a href="articles.html">文章资讯</a>
                <a href="privacy.html">隐私政策</a>
                <a href="terms.html">服务条款</a>
                <a href="disclaimer.html">免责声明</a>
                <a href="contact.html">联系我们</a>
                <a href="sitemap.html">网站地图</a>
            </div>
            <div class="footer-copyright">
                © 2024-2026 009tg.com 版权所有 | Invisible Man
            </div>
            <div class="footer-disclaimer">
                本站仅供学习交流使用，所有内容均来自互联网，如有侵权请联系删除
            </div>
        </div>
    </footer>'''
    else:
        footer_html = f'''<footer class="site-footer">
        <div class="footer-container">
            <div class="footer-links">
                <a href="index.html">Home</a>
                <a href="about.html">About</a>
                <a href="articles.html">Articles</a>
                <a href="privacy.html">Privacy</a>
                <a href="terms.html">Terms</a>
                <a href="disclaimer.html">Disclaimer</a>
                <a href="contact.html">Contact</a>
                <a href="sitemap.html">Sitemap</a>
            </div>
            <div class="footer-copyright">
                © 2024-2026 009tg.com All Rights Reserved | Invisible Man
            </div>
            <div class="footer-disclaimer">
                For learning purposes only, all content from the internet, contact us for removal if infringement
            </div>
        </div>
    </footer>'''

    html = f'''<!DOCTYPE html>
<html lang="{html_lang}">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="author" content="Invisible man" />
    <title>{page['title']}</title>
    <meta name="theme-color" content="#f9f9f9"/>
    <meta name="keywords" content="009tg下海导航,网址导航,上网导航,网址大全,网址目录,创业工具,副业赚钱,投资理财,跨境电商,营销工具,AI工具,社交媒体,独立站,广告投放"/>
    <meta name="description" content="{page['og_desc']}"/>
    <link rel="shortcut icon" href="{lang_prefix}assets/images/favicon.png">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5301924424938934"
         crossorigin="anonymous"></script>
    <link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Arimo:400,700,400italic">
    <link rel="stylesheet" href="{lang_prefix}assets/css/fonts/linecons/css/linecons.css">
    <link rel="stylesheet" href="{lang_prefix}assets/css/fonts/fontawesome/css/font-awesome.min.css">
    <link rel="stylesheet" href="{lang_prefix}assets/css/bootstrap.css">
    <link rel="stylesheet" href="{lang_prefix}assets/css/xenon-core.css">
    <link rel="stylesheet" href="{lang_prefix}assets/css/xenon-components.css">
    <link rel="stylesheet" href="{lang_prefix}assets/css/xenon-skins.css">
    <link rel="stylesheet" href="{lang_prefix}assets/css/nav.css">
    <script src="{lang_prefix}assets/js/jquery-1.11.1.min.js"></script>

    <script>
    var _hmt = _hmt || [];
    (function() {{
      var hm = document.createElement("script");
      hm.src = "https://hm.baidu.com/hm.js?c05bb16ea908292af9f6c513087a1cc3";
      var s = document.getElementsByTagName("script")[0];
      s.parentNode.insertBefore(hm, s);
    }})();
    </script>
    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
        <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
    <!-- / FB Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="http://009tg.com/{lang}/{page_key}.html">
    <meta property="og:title" content="{page['og_title']}">
    <meta property="og:description" content="{page['og_desc']}">
    <meta property="og:image" content="http://009tg.com/assets/images/webstack_banner_cn.png">
    <meta property="og:site_name" content="009tg下海导航">
    <!-- / Twitter Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{page['og_title']}">
    <meta name="twitter:description" content="{page['og_desc']}">
    <meta name="twitter:image" content="http://009tg.com/assets/images/webstack_banner_cn.png">
    <style>
        /* ========== 深色模式主题变量 ========== */
        :root {{
            --bg-main: #f4f4f4;
            --bg-content: #ffffff;
            --bg-sidebar: #303641;
            --bg-card: #ffffff;
            --bg-card-hover: #f8f9fa;
            --bg-navbar: #ffffff;
            --bg-input: #ffffff;
            --text-primary: #373e4a;
            --text-secondary: #6c757d;
            --text-muted: #979898;
            --border-color: #e4e6e9;
            --border-card: #e4e6e9;
            --link-color: #337ab7;
            --link-hover: #23527c;
            --shadow-card: 0 1px 3px rgba(0,0,0,0.08);
            --shadow-card-hover: 0 4px 12px rgba(0,0,0,0.15);
        }}
        [data-theme="dark"] {{
            --bg-main: #1a1d23;
            --bg-content: #22262e;
            --bg-sidebar: #16181d;
            --bg-card: #2a2f38;
            --bg-card-hover: #333945;
            --bg-navbar: #22262e;
            --bg-input: #2a2f38;
            --text-primary: #e0e0e0;
            --text-secondary: #a0a0a0;
            --text-muted: #707070;
            --border-color: #3a3f48;
            --border-card: #3a3f48;
            --link-color: #5dade2;
            --link-hover: #85c1e9;
            --shadow-card: 0 1px 3px rgba(0,0,0,0.3);
            --shadow-card-hover: 0 4px 12px rgba(0,0,0,0.5);
        }}
        [data-theme="dark"] body {{
            background-color: var(--bg-main) !important;
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] .main-content {{
            background-color: var(--bg-content) !important;
        }}
        [data-theme="dark"] .navbar.user-info-navbar {{
            background-color: var(--bg-navbar) !important;
            border-bottom-color: var(--border-color) !important;
        }}
        [data-theme="dark"] .user-info-menu a {{
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] .user-info-menu a:hover {{
            color: var(--link-color) !important;
        }}
        [data-theme="dark"] .panel {{
            background-color: var(--bg-card) !important;
            border-color: var(--border-card) !important;
        }}
        [data-theme="dark"] .panel-heading {{
            background-color: var(--bg-card) !important;
            border-bottom-color: var(--border-color) !important;
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] .panel-title,
        [data-theme="dark"] .panel h4 {{
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] .panel-body {{
            color: var(--text-secondary) !important;
        }}
        [data-theme="dark"] .panel-body p,
        [data-theme="dark"] .panel-body li,
        [data-theme="dark"] .panel-body span {{
            color: var(--text-secondary) !important;
        }}
        [data-theme="dark"] .panel-body a {{
            color: var(--link-color) !important;
        }}
        [data-theme="dark"] .panel-body a:hover {{
            color: var(--link-hover) !important;
        }}
        [data-theme="dark"] .panel-body h1,
        [data-theme="dark"] .panel-body h2,
        [data-theme="dark"] .panel-body h3,
        [data-theme="dark"] .panel-body h4,
        [data-theme="dark"] .panel-body h5,
        [data-theme="dark"] .panel-body h6 {{
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] .text-gray,
        [data-theme="dark"] .text-muted {{
            color: var(--text-muted) !important;
        }}
        [data-theme="dark"] .breadcrumb {{
            background-color: var(--bg-card) !important;
            border-color: var(--border-color) !important;
        }}
        [data-theme="dark"] .breadcrumb a {{
            color: var(--link-color) !important;
        }}
        [data-theme="dark"] .main-footer {{
            background-color: var(--bg-sidebar) !important;
            color: var(--text-secondary) !important;
        }}
        [data-theme="dark"] .main-footer a {{
            color: var(--link-color) !important;
        }}
        [data-theme="dark"] .table {{
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] .table td,
        [data-theme="dark"] .table th {{
            border-color: var(--border-color) !important;
            background-color: var(--bg-card) !important;
        }}
        [data-theme="dark"] .well {{
            background-color: var(--bg-card) !important;
            border-color: var(--border-color) !important;
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] .alert-info {{
            background-color: #1e3a5f !important;
            border-color: #2c5282 !important;
            color: #90cdf4 !important;
        }}
        [data-theme="dark"] .alert-warning {{
            background-color: #5f4a1e !important;
            border-color: #82682c !important;
            color: #f6e05e !important;
        }}
        [data-theme="dark"] .alert-success {{
            background-color: #1e5f3a !important;
            border-color: #2c8252 !important;
            color: #9ae6b4 !important;
        }}
        [data-theme="dark"] .alert-danger {{
            background-color: #5f1e1e !important;
            border-color: #822c2c !important;
            color: #feb2b2 !important;
        }}
        [data-theme="dark"] .form-control,
        [data-theme="dark"] input,
        [data-theme="dark"] select,
        [data-theme="dark"] textarea {{
            background-color: var(--bg-input) !important;
            border-color: var(--border-color) !important;
            color: var(--text-primary) !important;
        }}
        [data-theme="dark"] .horizontal-menu {{
            background-color: var(--bg-sidebar) !important;
        }}
        [data-theme="dark"] .navbar-brand .logo img {{
            filter: brightness(1.5);
        }}
        /* 主题切换按钮 */
        .theme-toggle-btn {{
            cursor: pointer;
            padding: 8px 12px;
            border-radius: 4px;
            transition: all 0.3s ease;
            background: transparent;
            border: none;
            font-size: 16px;
        }}
        .theme-toggle-btn:hover {{
            background-color: rgba(0,0,0,0.05);
        }}
        [data-theme="dark"] .theme-toggle-btn:hover {{
            background-color: rgba(255,255,255,0.1);
        }}
        .site-footer {{
            background-color: #f8f9fa;
            border-top: 1px solid #e9ecef;
            padding: 30px 0 20px;
            margin-top: 40px;
        }}
        [data-theme="dark"] .site-footer {{
            background-color: var(--bg-sidebar) !important;
            border-top-color: var(--border-color) !important;
        }}
        .site-footer .footer-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        .site-footer .footer-links {{
            text-align: center;
            margin-bottom: 15px;
        }}
        .site-footer .footer-links a {{
            color: #666;
            text-decoration: none;
            margin: 0 12px;
            font-size: 14px;
            transition: color 0.2s;
        }}
        .site-footer .footer-links a:hover {{
            color: #007bff;
        }}
        [data-theme="dark"] .site-footer .footer-links a {{
            color: var(--text-secondary) !important;
        }}
        [data-theme="dark"] .site-footer .footer-links a:hover {{
            color: var(--link-color) !important;
        }}
        .site-footer .footer-copyright {{
            text-align: center;
            color: #999;
            font-size: 13px;
            margin-bottom: 8px;
        }}
        [data-theme="dark"] .site-footer .footer-copyright {{
            color: var(--text-muted) !important;
        }}
        .site-footer .footer-disclaimer {{
            text-align: center;
            color: #aaa;
            font-size: 12px;
        }}
        [data-theme="dark"] .site-footer .footer-disclaimer {{
            color: var(--text-muted) !important;
            opacity: 0.8;
        }}
    </style>
</head>

<body class="page-body boxed-container">
    <nav class="navbar horizontal-menu navbar-fixed-top">
        <div class="navbar-inner">
            <div class="navbar-brand">
                <a href="{lang_prefix}index.html" class="logo">
                    <img src="{lang_prefix}assets/images/logo_dark_light@2x.png" width="100%" alt="" class="hidden-xs">
                    <img src="{lang_prefix}assets/images/logo@2x.png" width="100%" alt="" class="visible-xs">
                </a>
            </div>
            <div class="navbar-mobile-clear"></div>
        </div>
    </nav>
    <div class="page-container">
        <div class="main-content" style="">
            <nav class="navbar user-info-navbar" role="navigation">
                <ul class="user-info-menu left-links list-inline list-unstyled">
                    <li class="hidden-sm hidden-xs">
                        <a href="#" data-toggle="sidebar">
                            <i class="fa-bars"></i>
                        </a>
                    </li>
                    {lang_switcher}
                </ul>
                <ul class="user-info-menu right-links list-inline list-unstyled">
                    <li class="hidden-sm hidden-xs">
                        <button class="theme-toggle-btn" onclick="toggleTheme()" title="切换深色/浅色模式">
                            <i class="fa-moon-o" id="theme-icon"></i>
                        </button>
                    </li>
                </ul>
            </nav>
            <div class="row">
                <div class="col-md-12">
                    <div class="panel panel-default">
                        <h4 class="text-gray">{page['heading']}</h4>
                        <div class="panel-body">
                            <div class="row">
                                <div class="col-sm-12">
                                    {page['content']}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Bottom Scripts -->
    <script src="{lang_prefix}assets/js/bootstrap.min.js"></script>
    <script src="{lang_prefix}assets/js/TweenMax.min.js"></script>
    <script src="{lang_prefix}assets/js/resizeable.js"></script>
    <script src="{lang_prefix}assets/js/joinable.js"></script>
    <script src="{lang_prefix}assets/js/xenon-api.js"></script>
    <script src="{lang_prefix}assets/js/xenon-toggles.js"></script>
    <!-- JavaScripts initializations and stuff -->
    <script src="{lang_prefix}assets/js/xenon-custom.js"></script>
    <!-- 深色模式主题切换 -->
    <script>
        function initTheme() {{
            var savedTheme = localStorage.getItem('theme');
            if (savedTheme) {{
                document.documentElement.setAttribute('data-theme', savedTheme);
                updateThemeIcon(savedTheme);
            }} else {{
                if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {{
                    document.documentElement.setAttribute('data-theme', 'dark');
                    updateThemeIcon('dark');
                }}
            }}
        }}
        function toggleTheme() {{
            var currentTheme = document.documentElement.getAttribute('data-theme');
            var newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        }}
        function updateThemeIcon(theme) {{
            var icon = document.getElementById('theme-icon');
            if (icon) {{
                if (theme === 'dark') {{
                    icon.className = 'fa-sun-o';
                    icon.parentElement.title = '切换到浅色模式';
                }} else {{
                    icon.className = 'fa-moon-o';
                    icon.parentElement.title = '切换到深色模式';
                }}
            }}
        }}
        initTheme();
        if (window.matchMedia) {{
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {{
                if (!localStorage.getItem('theme')) {{
                    if (e.matches) {{
                        document.documentElement.setAttribute('data-theme', 'dark');
                        updateThemeIcon('dark');
                    }} else {{
                        document.documentElement.removeAttribute('data-theme');
                        updateThemeIcon('light');
                    }}
                }}
            }});
        }}
    </script>
    {footer_html}
</body>

</html>
'''
    return html


def main():
    print("=" * 60)
    print("生成标准页面（中英文）")
    print("=" * 60)

    for page_key in PAGES:
        for lang in ['cn', 'en']:
            output_dir = os.path.join(PROJECT_ROOT, lang)
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f'{page_key}.html')

            html = generate_page(page_key, lang)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)

            print(f"  已生成: {lang}/{page_key}.html ({len(html)} bytes)")

    print()
    print("生成完成！共生成 {} 个页面".format(len(PAGES) * 2))
    print()
    print("页面列表:")
    for page_key in PAGES:
        print(f"  - cn/{page_key}.html")
        print(f"  - en/{page_key}.html")


if __name__ == '__main__':
    main()
